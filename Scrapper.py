from bs4 import BeautifulSoup
import requests
import gspread
import math
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials


# Setup Google Sheets API
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('/Users/mr.lu/repos/Python-Web-Scrapper-Card-Prices/web-scrapper-387417-e47217ebe055.json', scopes=scope)

gc = gspread.authorize(creds)
sheet = gc.open("OP-01: Romance Dawn").sheet1


# Fetch card prices from TCGPlayer
url = 'https://shop.tcgplayer.com/price-guide/one-piece-card-game/romance-dawn'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.find_all('tr')

for row in rows[1:]:
    data = row.find_all('td')
    card_name = data[0].text
    try:
        sell_price = float(data[4].text.replace("$", ""))
    except ValueError:
        continue

    # Round up card price
    sell_price = math.ceil(sell_price / 0.25) * 0.25

    # Normalize card name
    if '-' in card_name:
        card_name_parts = card_name.split('-')
        card_name = card_name_parts[0].strip() + " (" + card_name_parts[1].strip() + ")"

        if 'Parallel' in card_name_parts[-1]:
            card_name += " (Parallel)"
        elif 'Box Topper' in card_name_parts[-1]:
            card_name += " (Box Topper)"
    
    # Find the card in the Google Sheet and update the sell price
    cell = sheet.findall(card_name)
    for c in cell:
        sheet.update_cell(c.row, 4, sell_price)