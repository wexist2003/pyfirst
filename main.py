def split_list(grade):
    list_lower = []
    list_higher = []
    if not grade == []:
        sum = 0
        for el in grade:
            sum += el
        avg = sum / len(grade)
        for el in grade:
            if el <= avg:
                list_lower.append(el)
            else:
                list_higher.append(el)
    kortlist = (list_lower, list_higher)
    return kortlist


a = []
print(split_list(a))
