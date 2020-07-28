from selenium import webdriver
from dotenv import load_dotenv
import os

load_dotenv()
CHROME_DRIVER_DIR = os.getenv('CHROME_DRIVER_DIR')

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(CHROME_DRIVER_DIR, chrome_options=options)
