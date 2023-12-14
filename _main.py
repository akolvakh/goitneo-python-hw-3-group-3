from _commands import *

def main():
    filename = "address_book.pkl"
    book = AddressBook.load_from_file(filename)
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        result = handle_command(user_input, book, filename)
        print(result)
        if result == "Good bye!":
            break
            
if __name__ == "__main__":
    main()