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
                result.append(f'{line[0]}:{line[1]}')
    return result
    

print(get_credentials_users("biner.txt"))
