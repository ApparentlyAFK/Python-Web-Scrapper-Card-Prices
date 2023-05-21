from bs4 import BeautifulSoup
import requests
import gspread
import math
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials


html_text = requests.get('...').text
soup = BeautifulSoup(html_text, 'lxml')
name = soup.find_all()
price = soup.find_all()