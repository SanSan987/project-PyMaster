from address_book import AddressBook, Record, Birthday, Name, Phone, Field


class NotFoundError(Exception):
    pass

class ContactsEmptyError(Exception):
    pass

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Such name is not found."
        except IndexError:
            return "Such name is not found."
        except NotFoundError:
            return "Contact not found."
        except ContactsEmptyError:
            return "Contacts is empty. Add some Contacts"

    return inner


def parse_input(user_input:str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_birthday(args:list, book:AddressBook) -> str:
    name, birthday = args
    new_birthday = Birthday(birthday)
    finded_contact = book.find(name)
    finded_contact.add_birthday(new_birthday)
    return "Birthday added."

@input_error 
def show_birthday(args:list, book:AddressBook) -> str:
    name = args[0]
    finded_contact = book.find(name)
    return finded_contact.show_birthday()

@input_error
def add_contact(args:list, book:AddressBook) -> str:
    name = args[0]
    phone = args[1]
    birthday = None
    
    if len(args) == 3:
        birthday = args[2]
        
    if birthday != None:
        new_record = Record(name, Birthday(birthday))
    else:
        new_record = Record(name)
        
    new_record.add_phone(phone)
    book.add_record(new_record)
    return "Contact added."

@input_error
def chnge_contact(args:list, book:AddressBook) -> str:
    name, phone = args
    finded_contact = book.find(name)
    finded_contact.change_phone(phone)
    return "Contact changed."
        
   
@input_error 
def phone(args:list, book:AddressBook) -> str:
    name = args[0]
    finded_contact = book.find(name)
    return finded_contact
        
        
@input_error   
def all(book:AddressBook) -> str:
    if len(book.data) > 0:
        text_res = ""
        all_records = book.all()
        for _, reco in all_records.items():
            text_res += f"{reco}\n"

        return text_res
    else:
        raise ContactsEmptyError
    
@input_error   
def birthdays(book:AddressBook) -> str:
    week_list = book.get_birthdays_per_week()
    if len(week_list) == 0:
        return "No birthdays"
    text_res = ""
    for dayweek, names in week_list.items():
        text_res += f"{dayweek}: {names}\n"
    return text_res
    