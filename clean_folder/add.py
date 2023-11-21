def my_generator():
    for i in range(1, 6):
        yield i

t = my_generator()
for item in t:
    print(item)