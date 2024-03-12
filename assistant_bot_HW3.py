from collections import defaultdict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.is_valid_phone():
            raise ValueError("Invalid phone number")
    
    def is_valid_phone(self):
        return len(self.value) == 10 and self.value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.is_valid_birthday():
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
    
    def is_valid_birthday(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {phone_str}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {phone_str}"

class AddressBook(defaultdict):
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name)

    def delete(self, name):
        if name in self.records:
            del self.records[name]

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        birthdays = defaultdict(list)

        for record in self.records.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                if today <= birthday_date < next_week:
                    day_of_week = birthday_date.strftime('%A')
                    birthdays[day_of_week].append(record.name.value)

        return birthdays

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter user name."
        except IndexError:
            return "Invalid command."
    
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, address_book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, address_book):
    name, phone = args
    record = address_book.find(name)
    if record:
        record.edit_phone(record.find_phone(phone), phone)
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return '; '.join(str(p) for p in record.phones)
    else:
        return "Contact not found."

@input_error
def show_all(address_book):
    if not address_book.records:
        return "No contacts found."
    else:
        return "\n".join([str(record) for record in address_book.records.values()])

@input_error
def add_birthday(args, address_book):
    name, birthday = args
    record = address_book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value}"
    elif record:
        return f"{name} has no birthday set."
    else:
        return "Contact not found."

def birthdays(address_book):
    upcoming_birthdays = address_book.get_birthdays_per_week()
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    else:
        result = "Upcoming birthdays:\n"
        for day, names in upcoming_birthdays.items():
            result += f"{day}: {', '.join(names)}\n"
        return result

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(show_phone(args, address_book))
        elif command == "all":
            print(show_all(address_book))
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(birthdays(address_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()



