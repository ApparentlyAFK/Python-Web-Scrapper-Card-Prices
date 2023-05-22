from bs4 import BeautifulSoup
import requests
import gspread
import math
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials


# Function to normalize a card name
def normalize_card_name(name):
    name = name.strip()  
    name = name.replace('.',' ')
    name = name.replace('-', ' - ')
    name = ' '.join(word.title() for word in name.split())
    
    # Check for "Parallel" and "Box Topper" after converting to title case
    if "Parallel" in name:
        name = name.replace('Parallel', '(Parallel)')
    if "Box Topper" in name:
        name = name.replace('Box Topper', '(Box Topper)')
    
    return name


# Setup Google Sheets API
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('JSON_credential_path', scopes=scope)

gc = gspread.authorize(creds)
sheet = gc.open("OP-01: Romance Dawn").sheet1


# Fetch card prices from TCGPlayer
url = 'https://shop.tcgplayer.com/price-guide/one-piece-card-game/romance-dawn'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.find_all('tr')


# Fetch all data from the Google Sheet
all_data = sheet.get_all_values()


# Convert it to a dictionary with card names as keys and row numbers as values
data_dict = {normalize_card_name(row[0]): i+1 for i, row in enumerate(all_data)}


# Print the dictionary to see how it's being processed
print("Dictionary from Google Sheets data:")
for key, value in data_dict.items():
    print(f"{key}: {value}")


# Batch requests
updates = []

for row in rows[1:]:
    data = row.find_all('td')
    card_name = data[0].text
    print(card_name)
    try:
        sell_price = float(data[4].text.replace("$", ""))
    except ValueError:
        continue

    # Round up card price
    sell_price = round(sell_price / 0.25) * 0.25

    # Normalize card name
    card_name = normalize_card_name(card_name)

    print(f"Searching for {card_name} in Google Sheet...")

    # Find the card in the local data
    row_number = data_dict.get(card_name)
    if row_number is not None:
        print(f"Adding update for {card_name} in row {row_number}...")
        updates.append(Cell(row=row_number, col=4, value=sell_price))
    else:
        print(f"Card not found in local data: {card_name}")

# Apply all updates at once
if updates:
    print("Applying updates...")
    sheet.update_cells(updates)
else:
    print("No updates to apply.")