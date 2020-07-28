from datetime import datetime, date
from bisect import bisect
from bs4 import BeautifulSoup
from selenium_driver import driver
import json


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


def get_stored_daily_readings(sign, current_date):
  # check if daily reading exists for a sign
  with open('daily_readings.json') as json_file:
    saved_readings = json.load(json_file)
    if current_date in saved_readings[sign]:
        return saved_readings[sign][current_date]
    else:
      return False


def store_daily_readings(sign, current_date, horoscope):
  # stores daily readings
  # handle exceptions
  with open('daily_readings.json', 'r+') as json_file:
    saved_readings = json.load(json_file)
    saved_readings[sign].update({current_date: horoscope})
    json_file.seek(0)
    json.dump(saved_readings, json_file, indent=2)
    json_file.truncate()


def get_daily_reading(user_command):
  # horoscope.com's order of the zodiac sign
  sign_order = {'aries': '1', 'taurus': '2', 'gemini': '3', 'cancer': '4', 'leo': '5',
                'virgo': '6', 'libra': '7', 'scorpio': '8', 'sagittarius': '9',
                'capricorn': '10', 'aquarius': '11', 'pisces': '12'}

  sign = user_command.split(' ')[0].lower()
  current_date = str(date.today())

  # check if daily reading already exists
  if get_stored_daily_readings(sign, current_date):
    stored_reading = get_stored_daily_readings(sign, current_date)
    return stored_reading

  # web scraping daily reading from horoscope.com
  url = 'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign='
  sign_url = url + sign_order[sign]
  driver.get(sign_url)
  soup = BeautifulSoup(driver.page_source, "lxml")
  driver.close()
  p_tags = soup.find(class_='main-horoscope').find_all('p')
  # may need to change
  horoscope = str(p_tags[0])[35:-4]

  # store daily reading in json file
  store_daily_readings(sign, current_date, horoscope)

  return horoscope


get_daily_reading('Pisces daily reading')
