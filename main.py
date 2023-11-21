def handler(command_list):
    len_command = len(command_list)
    match len_command:
        case 2:
            user_name = command_list[1]
        case 3:
            user_name = command_list[1]
            user_phone = command_list[2]
        case _:
            pass

    match command_list[0]:
        case "add":
            try:
                return func_add(user_name, user_phone)
            except UnboundLocalError:
                return "Give me name and phone please"
        case "change":
            try:
                return func_change(user_name, user_phone)
            except UnboundLocalError:
                return "Give me name and phone please"
        case "exit":
            return func_exit()
        case "good bye":
            return func_exit()
        case "close":
            return func_exit()
        case "hello":
            return func_hello()
        case "phone":
            try:
                return func_phone(user_name)
            except UnboundLocalError:
                return "Enter user name"
        case "show all":
            return func_show_all()
        case _:
            return "Enter correct command"
    return


def func_add(user_name, user_phone):
    new_contact = {user_name: user_phone}
    phone_book.update(new_contact)
    return "Added"


def func_change(user_name, user_phone):
    phone_book[user_name] = user_phone
    return "Changed"


def func_exit():
    return "Good bye!"


def func_hello():
    return "How can I help you?"


def main():
    while True:
        user_command = input("Enter your command:")
        match user_command:
            case ".":
                break
            case _:
                if user_command.lower().startswith(
                    "good bye"
                ) or user_command.lower().startswith("show all"):
                    alt_list = user_command.split(" ")
                    command_list[0] = f"{alt_list[0].lower()} {alt_list[1].lower()}"
                else:
                    command_list = user_command.split(" ")
                    command_list[0] = command_list[0].lower()
                result = handler(command_list)
                match result:
                    case "Good bye!":
                        print(result)
                        break
                    case _:
                        print(result)


def func_phone(user_name):
    return phone_book[user_name]


def func_show_all():
    result = ""
    for name, phone in phone_book.items():
        result = result + f"{name}: {phone}, "
    return result.removesuffix(", ")


phone_book = {}
main()
