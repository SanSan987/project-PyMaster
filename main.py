import bot_functions
import address_book


def main():

    book = address_book.AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = bot_functions.parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(bot_functions.add_contact(args, book))

        elif command == "change":
            print(bot_functions.chnge_contact(args, book))

        elif command == "phone":
            print(bot_functions.phone(args, book))

        elif command == "all":
            print(bot_functions.all(book))
            
        elif command == "add-birthday":
            print(bot_functions.add_birthday(args, book))
            
        elif command == "show-birthday":
            print(bot_functions.show_birthday(args, book))
        
        elif command == "birthdays":
            print(bot_functions.birthdays(book))
            
        else:
            print("Error: Invalid command.")

if __name__ == "__main__":
    main()