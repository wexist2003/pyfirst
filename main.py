from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):
    if users == []:
        return {}
   
    today = date.today()

    # calculation interval bases
    interval = []
    result = {}
    result_keys = []
    for i in range(7):
        limit_day = today + timedelta(days=i)
        limit_day_month = limit_day.month
        limit_day_day = limit_day.day
        week_day = limit_day.strftime("%A ").strip()
        limit_day_weekday = {week_day: []}
        element = f"{limit_day_month}{limit_day_day}"
        interval.append(element)
        result.update(limit_day_weekday)
        result_keys.append(week_day)

    # main sort
    for note in users:
        name = note.get("name")
        birth = note.get("birthday")
        birth_month = birth.month
        birth_day = birth.day
        el = f"{birth_month}{birth_day}"

        # adding to result
        if interval.count(el):
            position = interval.index(el)
            key = result_keys[position]
            result[key].append(name)

    # re-bring of weekends
    saturday = datetime(2023, 11, 11).date().strftime("%A ").strip()
    sunday = datetime(2023, 11, 12).date().strftime("%A ").strip()
    monday = datetime(2023, 11, 13).date().strftime("%A ").strip()
    tuesday = datetime(2023, 11, 14).date().strftime("%A ").strip()
    wednesday = datetime(2023, 11, 15).date().strftime("%A ").strip()
    thursday = datetime(2023, 11, 16).date().strftime("%A ").strip()
    friday = datetime(2023, 11, 17).date().strftime("%A ").strip()

    mon = result[monday]
    sat = result[saturday]
    sun = result[sunday]
    result[monday] = []
    result[monday].extend(sat)
    result[monday].extend(sun)
    result[monday].extend(mon)
    result.pop(saturday)
    result.pop(sunday)
    if not len(result[tuesday]):
        result.pop(tuesday)
    if not len(result[wednesday]):
        result.pop(wednesday)
    if not len(result[thursday]):
        result.pop(thursday)
    if not len(result[friday]):
        result.pop(friday)
    if not len(result[monday]):
        result.pop(monday)        

    count = 0
    for key, val in result.items():
        count += len(val)
    if count == 0:
        return {}

    return result


if __name__ == "__main__":
    users = [
        {"name": "John", "birthday": datetime(2021, 12, 31).date()},
        {"name": "Doe", "birthday": datetime(2021, 1, 1).date()},
        {"name": "Alice", "birthday": datetime(2021, 12, 29).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
