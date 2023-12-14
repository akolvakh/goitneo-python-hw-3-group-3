from datetime import datetime, timedelta
from collections import defaultdict    
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def validate(self, value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value=None):
        if value and not self.validate(value):
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)

    def validate(self, value):
        # # Add validation logic for DD.MM.YYYY format
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None  # Add birthday attribute to Record

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def birthday_add(self, birthday):
        self.birthday = Birthday(birthday)

    def birthday_show(self):
        return str(self.birthday) if self.birthday else "Birthday not set."

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday_show()}"

class AddressBook:
    def __init__(self):
        self.data = {}

    @classmethod
    def load_from_file(cls, filename):
        address_book = cls()
        try:
            with open(filename, 'rb') as file:
                address_book.data = pickle.load(file)
        except FileNotFoundError:
            pass
        return address_book

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)
    
    def add_record(self, record):
        #     self.data[record.name.value] = record
        # Check if the name of the record already exists in self.data
        if record.name.value not in self.data:
            # If it doesn't exist, add the record
            self.data[record.name.value] = record
            return "Contact added."
        else:
            return f"Contact '{record.name.value}' already exists."

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        if name in self.data:
            return self.data[name]

    def get_next_weekday(self, d, weekday):
        days_until_target = (weekday - d.weekday() + 7) % 7
        return d + timedelta(days=days_until_target)

    def get_birthdays_per_week(self, users):
        today = datetime.today().date()
        next_week_start = self.get_next_weekday(today, 0) + timedelta(weeks=1)
        days_of_week = defaultdict(list)

        for user in users.data.values():
            name = str(user.name)
            if user.birthday == None:
                exit
            else:
                birthday = user.birthday
                date_parts = birthday.split('.')
                birthday = datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
                birthday = birthday.date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                day_of_week = (today + timedelta(days=delta_days)).strftime("%A")

                if delta_days < 7:
                    days_of_week[day_of_week].append(name)
                elif delta_days == 7:
                    next_birthday_weekday = birthday_this_year.weekday()
                    if next_birthday_weekday == 6:  # If birthday falls on Saturday
                        days_of_week['Monday'].append(name)
                    elif next_birthday_weekday == 7:  # If birthday falls on Sunday
                        days_of_week['Monday'].append(name)

        res = ""
        for day, names in days_of_week.items():
            if day == 'Sunday' and names:
                res = res + "\n" + 'Monday: ' + ', '.join(names)
            elif day == 'Saturday'and names:
                res = res + "\n" + 'Monday: ' + ', '.join(names)
            elif names:
                res = res + "\n" + day + ' ' + ', '.join(names)
        
        return res

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

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
            return f"Phone number for {name}: {record.phones}"
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