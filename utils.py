from datetime import date, datetime

def check_age(birthday_str):
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    return age