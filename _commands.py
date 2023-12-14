from _address_book import AddressBook
from _record import Record
from _field import Name, Phone, Birthday
from datetime import datetime, timedelta
import pickle

def input_parse(user_input, book, filename):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args, book, filename

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct data (name, phone or birthday) please."
        except KeyError as e:
            return f"Error: Key '{e.args[0]}' does not exist."
        except IndexError:
            return "Error: Insufficient arguments."

    return inner

@input_error
def contact_add(args, address_book):
    if len(args) == 2:
        name, phone = args
        record = Record(name)  # Create a Record instance with the provided name
        record.add_phone(phone)  # Add the phone number to the Record
        address_book.add_record(record)  # Add the Record to the AddressBook
        return "Contact added."
    else:
        return "Invalid command format for adding a contact."

@input_error
def contact_change(args, address_book):
    if len(args) == 2:
        name, phone = args
        record = address_book.find(name)
        if record:
            record.phones = [Phone(phone)]  # Update the phone number for the found record
            return f"Phone number updated for {name}."
        else:
            return f"{name} does not exist in contacts."
    else:
        return "Invalid command format for changing a contact's phone number."

@input_error
def phone_get(args, address_book):
    if len(args) == 1:
        name = args[0]
        record = address_book.find(name)
        if record:
            res = "Phone number for " + name + ": "
            for phone in record.phones:
                res = res + str(phone) + " "
            return res
        else:
            return f"{name} does not exist in contacts."
    else:
        return "Invalid command format for retrieving a phone number."

@input_error
def display_all(address_book):
    if address_book:
        result = "All contacts:\n"
        for record in address_book.data.values():
            result += f"{str(record)}\n"
        return result
    else:
        return "No contacts available."

@input_error
def birthday_add(args, address_book):
    if len(args) == 2:
        name, birthday = args

        record = address_book.find(name)
        if record:
            record.birthday_add(birthday)
            return f"Birthday added for {name}."
        else:
            return f"{name} does not exist in the address book."
    else:
        return "Invalid command format for adding a birthday."

@input_error
def birthday_show(args, address_book):
    if len(args) == 1:
        name = args[0]
        record = address_book.find(name)
        if record:
            return f"Birthday for {name}: {record.birthday_show()}"
        else:
            return f"{name} does not exist in the address book."
    else:
        return "Invalid command format for displaying a birthday."

@input_error
def birthdays(address_book):
    upcoming_birthdays = address_book.get_birthdays_per_week(address_book)
    if upcoming_birthdays:
        return "Upcoming birthdays:" + upcoming_birthdays
    else:
        return "No upcoming birthdays in the next week."

def handle_command(user_input, book, filename):
    command, *args = user_input.split()
    command = command.lower()

    if command in ["close", "exit"]:
        book.save_to_file(filename)
        return "Good bye!"
    elif command == "hello":
        return "How can I help you?"
    elif command == "save":
        book.save_to_file(filename)
        return "Address book saved."
    elif command == "load":
        book = AddressBook.load_from_file(filename)
        return "Address book loaded."
    elif command == "add":
        return contact_add(args, book.data)
    elif command == "change":
        return contact_change(args, book.data)
    elif command == "phone":
        return phone_get(args, book.data)
    elif command == "all":
        return display_all(book.data)
    elif command == "add-birthday":
        return birthday_add(args, book.data)
    elif command == "show-birthday":
        return birthday_show(args, book.data)
    elif command == "birthdays":
        return birthdays(book.data)
    else:
        return "Invalid command."
