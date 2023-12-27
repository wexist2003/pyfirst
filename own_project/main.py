from collections import UserDict
import re
from datetime import datetime
import pickle

# from abc import ABC, abstractmethod


#  Базовий клас для полів запису. Буде батьківським для всіх полів, у ньому реалізується логіка загальна для всіх полів
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __setitem__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value


# Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, name):
        self.value = name
        # print(f"name = {self.value}")


# Клас для зберігання дати народження контакту. НЕ обов'язкове поле.
class Birthday(Field):
    def __init__(self, birthday_date):
        self.value = birthday_date
        # print(f"bithday = {self.value}")

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, birthday_date):
        if isinstance(birthday_date, str) and len(birthday_date) > 0:
            self.value = birthday_date


# Клас для зберігання  номера телефону. Має валідацію формату (10 цифр). Необов'язкове поле з телефоном та таких один запис Record може містити декілька
class Phone(Field):
    def __init__(self, number):
        self.value = number

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, number):
        if len(re.findall("\d", number)) == 10:
            self.value = number
            # print(f"phone = {self.value}")
        else:
            raise ValueError("Invalid phone number format")


#  Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів. Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        # print(f"{self} record = {self.name} / {self.phones}")
        self.birthday = birthday
        # print(f"{self} birthday = {self.birthday}")

    def add_phone(self, user_phone):
        try:
            new_phone = Phone(user_phone)
            self.phones.append(new_phone)
            # print(f"{self} add_phone = {self.phones}")
        except ValueError as e:
            print(e)

    def remove_phone(self, user_phone):
        for phone in self.phones:
            if phone.value == user_phone:
                self.phones.remove(phone)
                # print(f"{self} remove_phone = {[p.value for p in self.phones]}")
                return
        raise ValueError

    def edit_phone(self, old_phone, new_phone):
        try:
            phone_to_edit = next((p for p in self.phones if p.value == old_phone), None)
            if phone_to_edit:
                phone_to_edit.value = new_phone
            else:
                raise ValueError
        except:
            raise ValueError

    def find_phone(self, user_phone):
        for i in self.phones:
            if i.value == user_phone:
                return i

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            birthday_date = datetime.strptime(self.birthday.value, "%d-%m-%Y")
            next_birthday = datetime(today.year, birthday_date.month, birthday_date.day)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


# Клас для зберігання та управління записами. Успадковується від UserDict, та містить логіку пошуку за записами до цього класу
class AddressBook(UserDict):
    def add_record(self, addname):
        self.data[addname.name.value] = addname
        # print(f"new dict = {self.data}")

    def find(self, user_name):
        return self.data.get(user_name)

    def find_by_nums(self, nums):
        result = []
        for record in self.data.values():
            for phone in record.phones:
                if nums in phone.value:
                    result.append(record)
                    break
        return result

    def find_by_literals(self, literals):
        result = []
        for record in self.data.values():
            if literals in record.name.value:
                result.append(record)
        return result

    def delete(self, user_name):
        if user_name in self.data:
            del self.data[user_name]

    def __iter__(self):
        return iter(self.data.values())

    def iterator(self, N):
        return Iterable(self, N)

    def save_to_disk(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self, fh)

    def load_from_disk(self, filename):
        with open(filename, "rb") as fh:
            unpacked = pickle.load(fh)
            return unpacked


class Iterable:
    def __init__(self, address_book, N):
        self.address_book = address_book
        self.N = N
        self.index = 0
        self.records = list(address_book.values())

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.records):
            start = self.index
            self.index += self.N
            return self.records[start : self.index]
        raise StopIteration
