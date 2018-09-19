import pandas as pd
import requests
from pandas.io.json import json_normalize
from datetime import datetime
import time

class Td:
    def __init__(self,refresh_token,client_id,apikey):
        # URL decoded refresh token
        self.refresh_token= refresh_token
        self.apikey= apikey
        self.client_id= client_id

    def get_access_token(self):
        #Post Access Token Request
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = { 'grant_type': 'refresh_token',  'refresh_token': self.refresh_token,
        'client_id': self.client_id}
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        print (authReply)
        return authReply

    def get_quotes(self,symbol):
        access_token = self.get_access_token().json()
        access_token = access_token['access_token']
        headers={'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(access_token)}
        data = { 'symbol': symbol,  'apikey': self.apikey}
        authReply = requests.get('https://api.tdameritrade.com/v1/marketdata/quotes',
        headers=headers, params=data)
        print(authReply)
        return (authReply.json())


    def unix_time_millis(self,dt):
        epoch = datetime.utcfromtimestamp(0)
        return int((dt - epoch).total_seconds() * 1000.0)

    def get_price_history(self,symbol,startDate=None,endDate=None):
        access_token = self.get_access_token().json()
        access_token = access_token['access_token']
        headers={'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': 'Bearer {}'.format(access_token)}
        data = { 'periodType': 'year','frequencyType':'daily',
        'startDate':startDate,'endDate':endDate}
        authReply = requests.get('https://api.tdameritrade.com/v1/marketdata/'+symbol+'/pricehistory',
        headers=headers, params=data)
        print(authReply.json())
        candles = authReply.json()
        df = json_normalize(authReply.json())
        #df = pd.DataFrame(candles['candles'])
        return df


token='kFMVMxIh1MJnIBZr2AlxYip/7DrK1mapNj7/ACpHzVA3VCP9V3qdfdRML6YGu6gM8iO7j8bZ2Woq5l2ABK6M6pdYVTzioxpVMA9eQee+Fqsi/nhvr6UV9bnJfkrNBp8Pd3sv26ThizJad+ipup0LvY1CAi1zdB0tZKWUy01V1OTGV3W6H3uiTz5gJXe5M5f+XoUvod0SFpyxz627grwx0aKTwxOBIcCuIiQ2BiiUIpGYn8pYeBNIzJosvnTyOvgqju8DJnHxQgWCCgrhAYqA46Q3k0U770ZkEIEiGOP8T6aL57f4EYae0q+xOctkYrapzSUhvrontUdIvTHHojbTwsfwWkpVcqi9BLb1d59JX9Rb4F3nGAMIJMlpGh1z7MGRPoZNWL1nM1Xhwjewup0UGDHnKJQAIGbXMRCgkaD74i6OBfe/CuJvbDo9MpJ100MQuG4LYrgoVi/JHHvlgLNUUcCUZViYC4FydMjG9oLIDGqCMbezXG9qu9z+Mx239nbDq0FjnLDx69ZMnTXmq1Qoswnt6gbLpA8DlFBFjgYqRl3dS83kM8eOkP374xjCCOFetZTwD4i5jjlBZkJLVepXO32E9yKMOZzPHdrLXb8FIRW+hmjLy1l20QgPxmSrTe5fR+YMAE8wps2AFIg12wo+5ar0lMuQ4ZX20hz4ol4sxWMCJWboCAn1jYYK0MldfkmTqhGe9uBvDFl0qZE1NPWUzIOR1l9+DcESuOi+dI9UYcDomJ5TtT+uOt3cx5HjBSxuVN8HddcghLdHlIxAQKP3XaH1gQSHdLBSDRmFG7gwIDR5QM52/t4tfqOElEMM0MUkmnSUnFasjOgymLkb+3GDqzQrklk1/OOimNT+xUgKCFc0snQoLaXHzwHimoM5p5946DUII9gZvBg=212FD3x19z9sWBHDJACbC00B75E'

apikey ='MJKIKI@AMER.OAUTHAP'
client_id = 'MJKIKI@AMER.OAUTHAP'

p = Td(token,client_id,apikey)
start_date = datetime.strptime('04 3 2018  1:33PM', '%m %d %Y %I:%M%p')
end_date = datetime.strptime('05 3 2018  1:33PM', '%m %d %Y %I:%M%p')
phist= p.get_price_history('AAPL',p.unix_time_millis(start_date),p.unix_time_millis(end_date))
print phist
