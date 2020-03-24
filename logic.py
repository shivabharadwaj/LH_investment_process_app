import pandas as pd
from dateutil.relativedelta import relativedelta
import textwrap
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google API to access google doc
def get_ticker_data(ticker):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Investment Process App').sheet1

    data = sheet.get_all_values()
    headers = data.pop(0)
    df_final = pd.DataFrame(data, columns=headers)
    df_final['Date']= pd.to_datetime(df_final['Date'])

    # Access company of interest
    ticker = ticker
    ticker_data = df_final[df_final['Ticker'] == ticker]

    return ticker_data

# Add line breaks to comments
def add_new_line(comment):
    split_text = textwrap.wrap(comment, width=25)
    final = '<br> '.join(split_text)
    return final

# Get most recent trading day (takes timestamp and return datetime)
def last_trading_day(date):
    closing_day_latest = date

    if (date.weekday() == 5):
        closing_day_latest = date - relativedelta(days=1)

    if (date.weekday() == 6):
        closing_day_latest = date - relativedelta(days=2)

    return closing_day_latest


# Get coordinates for textbox annotations
def get_y_position(counter, price_stock, max_price):
    y_pos = 0
    if ((price_stock <= (0.5 * max_price)) and counter % 2 == 0):
        y_pos = price_stock

    elif ((price_stock <= (0.5 * max_price)) and counter % 2 != 0):
        y_pos = price_stock * 1.1

    elif ((price_stock > (0.5 * max_price)) and counter % 2 == 0):
        y_pos = price_stock

    else:
        y_pos = price_stock * 0.9

    return y_pos

# Create dictionaries for drop down menu

