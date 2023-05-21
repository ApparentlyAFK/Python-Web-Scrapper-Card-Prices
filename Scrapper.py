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


# Fetch card prices from TCGPlayer
url = 'https://shop.tcgplayer.com/price-guide/one-piece-card-game/romance-dawn'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.find_all('tr')

for row in rows[1:]:
    data = row.find_all('td')
    card_name = data[0].text
    sell_price = float(data[4].text.replace("$", ""))

    # Round up card price
    sell_price = math.ceil(sell_price / 0.25) * 0.25

    # Find the card in the Google Sheet and update the sell price
    cell = sheet.find(card_name)
    sheet.update_cell(cell.row, 'column_number_of_sell_price', sell_price)