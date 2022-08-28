from collections import UserDict


class Field:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    pass


class AddressBook(UserDict):

    def add_contact(self, name: Name, phone: Phone = None):
        contact = Record(name=name, phone=phone)
        self.data[name.value] = contact

    def add_record(self, record: "Record"):
        self.data[record.name.value] = record

    def find_by_name(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None

    def find_by_phone(self, phone: str):
        for record in self.data.values():
            if phone in [number.value for number in record.phones]:
                return record
            return None


class Record:

    def __init__(self, name: Name, phone: Phone = None):
        self.name: Name = name
        self.phones: list[Phone] = [phone] if phone is not None else []


    def add_phone(self, phone_number: Phone):
        self.phones.append(phone_number)


    def change_phone(self, old_number: Phone, new_number: Phone):
        try:
            self.phones.remove(old_number)
            self.phones.append(new_number)
        except ValueError:
            return f"{old_number} does not exist"


    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"{phone} does not exist"







