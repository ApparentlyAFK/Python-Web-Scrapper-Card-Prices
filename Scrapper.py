from bs4 import BeautifulSoup
import requests
import gspread
import math
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials


# Setup Google Sheets API
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('python-web-scrapper@web-scrapper-387417.iam.gserviceaccount.com', scopes=scope)

gc = gspread.authorize(creds)
sheet = gc.open("your_google_sheet_name").sheet1