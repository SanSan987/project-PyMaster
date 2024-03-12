from collections import defaultdict
from datetime import datetime, timedelta

def get_birthdays_per_week(users):
    today = datetime.today().date()
    birthdays_per_week = defaultdict(list)


    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)
        
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        delta_days = (birthday_this_year - today).days
        
        birthday_weekday = (today + timedelta(days=delta_days)).strftime('%A')
        
        if delta_days < 7:
            birthday_weekday = 'Monday'
        
        birthdays_per_week[birthday_weekday].append(name)
    
    for day, names in birthdays_per_week.items():
        print(f"{day}: {', '.join(names)}")

users = [
    {"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
    {"name": "Jan Koum", "birthday": datetime(1976, 2, 24)},
    {"name": "Kim Kardashian", "birthday": datetime(1980, 10, 21)},
    {"name": "Jill Valentine", "birthday": datetime(1974, 5, 30)}
]
get_birthdays_per_week(users)
