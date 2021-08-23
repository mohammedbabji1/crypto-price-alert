import requests
import keys
import pandas as pd
from time import sleep

def get_crypto_price(base_currency='USD', assests='BTC,ETH,DOGE,SOL'):
    url = 'https://api.nomics.com/v1/currencies/ticker'

    payload = {'key':keys.NOMICS_KEY, 'ids': assests, 'interval':'1d', 'convert': base_currency}
    responce = requests.get(url, params=payload)
    data = responce.json()

    crypto_currency, crypto_price, crypto_timestamp = [], [], []

    #print(data)

    for asset in data:
        crypto_currency.append(asset['currency'])
        crypto_price.append(asset['price'])
        crypto_timestamp.append(asset['price_timestamp'])

    raw_data = {
        'assets' : crypto_currency,
        'rates' : crypto_price,
        'timestamp' : crypto_timestamp
    }

    df = pd.DataFrame(raw_data)
    return df

def set_alert(dataframe, asset, alert_high_price):
    crypto_value = float(dataframe[dataframe['assets'] == asset]['rates'].item())

    details = f'{asset}: {crypto_value}, Target: {alert_high_price}'

    if crypto_value >= alert_high_price:
        print(details + ' << TARGET VALUE REACHED!!')
    else:
        print(details)


#ALERT While loop
loop = 0

while True:
    print(f'------------------------------------ ({loop}) ------------------------------------')

    try:
        df = get_crypto_price()
        #Add your ticker in below
        set_alert(df, 'BTC', 49581.48)
        set_alert(df, 'ETH', 3345.00)
        set_alert(df, 'DOGE', 0.31760)
        set_alert(df, 'SOL', 72.45)

    except Exception as e:
        print(e)
        print('Couldn\'t retrive the value... Trying again')

    loop += 1
    sleep(10)


