from collections import UserDict
import re


#  Базовий клас для полів запису. Буде батьківським для всіх полів, у ньому реалізується логіка загальна для всіх полів
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, name):
        self.value = name
        print(f"name = {self.value}")


# Клас для зберігання номера телефону. Має валідацію формату (10 цифр). Необов'язкове поле з телефоном та таких один запис Record може містити декілька
class Phone(Field):
    # Реалізовано валідацію номера телефону (має бути 10 цифр).
    def __init__(self, number):
        value = ""
        numbers = re.findall("\d", number)
        if len(numbers) == 10:
            self.value = number
            print(f"phone = {self.value}")
        else:
            raise ValueError


#  Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів. Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        print(f"{self} record = {self.name} / {self.phones}")

    def add_phone(self, user_phone):
        new_phone = Phone(user_phone)
        self.phones.append(new_phone)
        print(f"{self} add_phone = {self.phones}")

    def remove_phone(self, user_phone):
        self.phones.remove(user_phone)
        print(f"{self} remove_phone = {self.phones}")

    def edit_phone(self, old_phone, new_phone):
        try:
            self.phones[old_phone] = new_phone
            print(f"{self} edit_phone = {self.phones}")
        except:
            raise ValueError

    def find_phone(self, user_phone):
        for i in self.phones:
            if i.value == user_phone:
                return i

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


# Клас для зберігання та управління записами. Успадковується від UserDict, та містить логіку пошуку за записами до цього класу
class AddressBook(UserDict):
    def add_record(self, addname):
        new_dict = {addname.name.value: addname.phones}
        print(f"{self} new dict = {new_dict}")
        self.data.update(new_dict)
        print(f"self.data = {self.data}")

    def find(self, user_name):
        print(f"self = {self}")
        print(f"FIND {user_name} in: {self.data}")
        for i in self.data:
            print(f"i = {i}")
            if i == user_name:
                print(f"GET {self.data[user_name]}")
                print(f"RETURN '{user_name}': {self.data[user_name]}'")
                return f"{user_name}: {self.data[user_name]}'"

    def delete(self, user_name):
        self.data.pop(user_name)
        return
