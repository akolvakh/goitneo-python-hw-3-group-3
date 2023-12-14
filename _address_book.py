from _record import Record
from collections import defaultdict
from datetime import datetime, timedelta
from _field import Name, Phone, Birthday
import pickle

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
                birthday = str(user.birthday)
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
