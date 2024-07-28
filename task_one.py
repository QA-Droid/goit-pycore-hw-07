from collections import UserDict
from datetime import datetime

class Field:
    """Record fields to address book"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Class to record name for address book"""
    def __init__(self, name: str):
        super().__init__(name)

class Phone(Field):
    """Class for address book record name field"""
    def __init__(self, phone: str):
        self.value = self.__validate_phone(phone)

    def __validate_phone(self, phone: str) -> str:
        """Phone validation"""
        if len(phone) != 10:
            raise ValueError("The phone number must contain 10 digits")

        if not phone.isdigit():
            raise ValueError("The phone number must contain only numbers")

        return phone

class Birthday(Field):
    """Class for address book record birthday field"""
    def __init__(self, birthday: str):
        self.value = self.__validate_birthday(birthday)

    def __validate_birthday(self, birthday: str) -> datetime:
        """Birthday validation and conversion to datetime"""
        try:
            return datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError as e:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from e

class Record:
    """Class for address book to add, remove, edit and find phone number and birthday"""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        """Method to add a phone number"""
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone: str):
        """Method to remove a phone number"""
        phone_obj = self.find_phone(phone)
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str):
        """Method to edit a phone number"""
        old_phone_obj = self.find_phone(old_phone)
        new_phone_obj = Phone(new_phone)
        index = self.phones.index(old_phone_obj)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone: str) -> Phone:
        """Method to find a phone number"""
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError("Phone number not found.")

    def add_birthday(self, birthday: str):
        """Method to add a birthday"""
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        """Method to calculate days to next birthday"""
        if not self.birthday:
            return None
        today = datetime.now().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):
    """Class for address book"""
    def add_record(self, record: Record):
        """Method to add a record"""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """Method to find a record"""
        if name in self.data:
            return self.data[name]
        raise ValueError("Record not found.")

    def delete(self, name: str):
        """Method to delete a record"""
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found.")

    def get_upcoming_birthdays(self, days: int = 7):
        """Method to get upcoming birthdays"""
        today = datetime.now().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                days_to_birthday = record.days_to_birthday()
                if days_to_birthday is not None and days_to_birthday <= days:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

def main():
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("0937777777")
    john_record.add_phone("5555555555")
    john_record.add_birthday("25.12.1990")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("01.01.1995")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("0937777777", "0936666666")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")
    print("Jane's record deleted.")

    for name, record in book.data.items():
        print(record)
    
    vova_record = Record("Vovan")
    vova_record.add_phone("0934563292")
    vova_record.add_birthday("31.07.1992")
    book.add_record(vova_record)

    upcoming_birthdays = book.get_upcoming_birthdays()
    for record in upcoming_birthdays:
        print(f"Upcoming birthday: {record}")

if __name__ == "__main__":
    main()