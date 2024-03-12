from datetime import datetime
from collections import UserDict


class BirthdayNotFoundError(Exception):
    pass

class BirthdayFormatError(Exception):
    pass

class ContactNotFoundError(Exception):
    pass

def book_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BirthdayNotFoundError:
            return "Birthday not added."
        except ContactNotFoundError:
            return "Contact not added."
        except BirthdayFormatError:
            return "Birthday date format is invalide"

    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        
class Birthday():
    def __init__(self, val):
        try:
            self.datetime_object = datetime.strptime(val, "%d.%m.%Y")
        except ValueError:
            raise BirthdayFormatError("Birthday date format is invalide")
        
        
    def __str__(self) -> str:
        return datetime.strftime(self.datetime_object, "%d.%m.%Y")

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        
        if self.is_valide(value):
            raise ValueError("Number is not valide format")
        
    def is_valide(self, num:str) -> bool:
        if not len(num) == 10:
            return True
        else:
            return False

class Record:
    def __init__(self, name:str, birthday:Birthday = None):
        self.name = Name(name)
        self.birthday = birthday
        self.phones = []
    
    @book_error    
    def show_birthday(self):
        if self.birthday != None:
            return f"Contact name: {self.name.value}, birthday: {self.birthday}"
        else:
            raise BirthdayNotFoundError
        
    def add_birthday(self, birthday:Birthday):
        self.birthday = birthday
    
    def add_phone(self, num:str):
        if not num in self.phones:
            new_num = Phone(num)
            if new_num != None:
                self.phones.append(new_num)
    
    def edit_phone(self, old_num:str, new_num:str):
        for phone in self.phones:
            if phone.value == old_num:
                pos = self.phones.index(phone)
                self.phones[pos] = Phone(new_num)
                
    def change_phone(self, num:str):
        self.phones.clear()
        new_num = Phone(num)
        self.phones.append(new_num)
    
    def find_phone(self, num:str) -> str:
        for phone in self.phones:
            if phone.value == num:
                return num

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
        
    def add_record(self, record:Record):
        if record.name.value in self.data:
            raise ValueError("Not Added, contact already exist. use command 'change' please")
        else:
            self.data[record.name.value] = record
        
    def find(self, name:str) -> Record:
        if name in self.data:
            return self.data[name]
        else:
            raise ContactNotFoundError
    
    def delete(self, name:str):
        self.data.pop(name)
        
    def all(self) -> dict:
        return self.data
        
    def get_birthdays_per_week(self):
    
        week_list = {}
        date_today = datetime.today().date()

        name:str
        contact:Record
        for name, contact in self.data.items():
            name = name
            birthday = contact.birthday.datetime_object.date()
            birthday_this_year = birthday.replace(year=date_today.year)

            if birthday_this_year < date_today:
                birthday_this_year = birthday.replace(year=date_today.year + 1)

            delta_days = (birthday_this_year - date_today).days

            if delta_days < 7:
                week_name = birthday_this_year.strftime("%A")

                if birthday_this_year.weekday() >= 5:
                    week_name = 'Monday'

                if week_name not in week_list.keys():
                    week_list[week_name] = name
                else:
                    week_list[week_name] += ", " + name
        return week_list 
        
    