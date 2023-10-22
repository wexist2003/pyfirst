import shutil


def write_employees_to_file(employee_list, path):
    th = open(path, "w")
    for dep in employee_list:
        for person in dep:
            th.write(person + "\n")
    th.close()
    return


def read_employees_from_file(path):
    th = open(path, "r")
    result = []
    while True:
        line = str(th.readline())
        print(line)
        if not line:
            break
        else:
            person = line.removesuffix("\n")
            result.append(person)
    th.close()
    return result


def add_employee_to_file(record, path):
    th = open(path, "a")
    th.write(record)
    th.close()
    return


def get_cats_info(path):
    with open(path, "r") as th:
        result = []
        while True:
            line = str(th.readline())
            if not line:
                break
            else:
                person = line.removesuffix("\n")
                person = person.split(",")
                dict_person = {"id": person[0], "name": person[1], "age": person[2]}
                result.append(dict_person)
    return result


def get_recipe(path, search_id):
    with open(path, "r") as th:
        result = ""
        while True:
            line = str(th.readline())
            if not line:
                if result == "":
                    result = None
                break
            else:
                person = line.removesuffix("\n")
                if person.startswith(search_id):
                    person = person.split(",")
                    ingridients = []
                    for ingr in range(len(person)):
                        if ingr > 1:
                            ingridients.append(person[ingr])
                    dict_person = {
                        "id": person[0],
                        "name": person[1],
                        "ingredients": ingridients,
                    }
                    result = dict_person
    return result


def sanitize_file(source, output):
    result = ""
    with open(source, "r") as th:
        while True:
            line = str(th.readline())
            if not line:
                break
            else:
                to = 0
                add = line
                for to in range(10):
                    add = add.replace(f"{to}", "")
                result = result + add
                print(result)
    with open(output, "w") as th2:
        th2.write(result)
    return


def save_applicant_data(source, output):
    result = ""
    for num in source:
        for key, value in num.items():
            result = result + str(value) + ","
        result = result.removesuffix(",") + "\n"

    with open(output, "w") as th2:
        th2.write(result)
    return


abbit = [
    {
        "name": "Kovalchuk Oleksiy",
        "specialty": 301,
        "math": 175,
        "lang": 180,
        "eng": 155,
    },
    {
        "name": "Ivanchuk Boryslav",
        "specialty": 101,
        "math": 135,
        "lang": 150,
        "eng": 165,
    },
    {
        "name": "Karpenko Dmitro",
        "specialty": 201,
        "math": 155,
        "lang": 175,
        "eng": 185,
    },
]


def is_equal_string(utf8_string, utf16_string):
    print(utf8_string.encode("utf-8").decode("utf-8"))
    print(utf16_string.encode("utf-16").decode("utf-16"))
    return


def save_credentials_users(path, users_info):
    with open(path, "wb") as th:
        for user, password in users_info.items():
            to_bin = user + ":" + password + "\n"
            th.write(to_bin.encode())
    return


def get_credentials_users(path):
    result = []
    with open(path, "rb") as th:
        while True:
            line = th.readline().decode()
            if not line:
                break
            else:
                line = line.split(":")
                line[1] = line[1].removesuffix("\n")
                result.append(f"{line[0]}:{line[1]}")
    return result


import base64


def encode_data_to_base64(data):
    result = []
    for code in data:
        rez = base64.b64encode(code.encode())
        rez = rez.decode("utf-8")
        result.append(rez)
    return result


import shutil


def create_backup(path, file_name, employee_residence):
    with open(f"{path}/{file_name}", "wb") as th:
        result = ""
        for key, val in employee_residence.items():
            to_save = f"{key} {val}\n"
            to_save = to_save.encode()
            th.write(to_save)
        result = shutil.make_archive("backup_folder", "zip", path)
    return result


print(
    is_equal_string(
        "hello",
        "\xff\xfeh\x00e\x00l\x00l\x00o\x00",
    )
)
