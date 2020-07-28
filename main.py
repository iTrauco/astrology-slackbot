from datetime import datetime
from bisect import bisect


def get_sun_sign(user_birth_date):
  # add docstring
  month, date = format_birth_date(user_birth_date)
  signs = [(1, 19, "Capricorn"), (2, 18, "Aquarius"), (3, 20, "Pisces"), (4, 19, "Aries"),
           (5, 20, "Taurus"), (6, 20, "Gemini"), (7, 22, "Cancer"), (8, 22, "Leo"), (9, 22, "Virgo"),
           (10, 22, "Libra"), (11, 21, "Scorpio"), (12, 21, "Sagittarius"), (12, 31, "Capricorn")]
  sun_sign = signs[bisect(signs, (month, date))][2]
  return sun_sign


def format_birth_date(user_birth_date):
  # add doctring
  # trim whitespace
  birth_date = user_birth_date.strip()
  date_array = birth_date.split(' ')
  month_name = date_array[0]
  day_num = int(date_array[1])

  # check if month_name is abbreviated or not
  if len(month_name) <= 3:
    abbrev = '%b'
  else:
    abbrev = '%B'

  # check if month is valid
  if not check_month(month_name, abbrev):
    return {'error': 'The stars ⭐ do no align with your birth month.'}

  month_object = datetime.strptime(month_name, abbrev)
  month_num = month_object.month

  # check if day is valid
  if not check_day(month_num, day_num):
    return {'error': 'The cosmos 🔮 cannot forsee your birth day.'}

  return month_num, day_num


def check_month(month_name, abbrev):
  try:
    month_object = datetime.strptime(month_name, abbrev)
    return True
  except ValueError:
    print('The stars ⭐ do no align with your birth month.')
    return False


def check_day(month_num, day_num):
  try:
    birthday = str(month_num) + '/' + str(day_num)
    day_object = datetime.strptime(birthday, '%m/%d')
    return True
  except ValueError:
    print('The cosmos 🔮 cannot forsee your birth day.')
    return False
