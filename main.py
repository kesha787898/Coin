import json
from dataclasses import dataclass
from typing import List

import requests

COINS_BINANCE = ['USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'DAI', 'SHIB']

FF_DOLLARS_IN_EURO = 1.02


class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
            # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount
@dataclass
class Adv:
    minSingleTransAmount: int
    maxSingleTransAmount: int
    tradableQuantity: int
    monthOrderCount: int
    monthFinishRate: float
    userGrade: int
    price: float
    banks: List[str]


def get_page_advertisments(asset, fiat, type, banks, page=0):
    data = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": True,
        "page": page,
        "payTypes": banks,
        "publisherType": None,
        "rows": 10,
        "tradeType": type,
        "transAmount": "5000"
    }
    response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', json=data)
    resp_data = json.loads(response.text)['data']
    advs = []
    if not resp_data:
        return advs
    for i in resp_data:
        maxSingleTransAmount = i['adv']['maxSingleTransAmount']
        minSingleTransAmount = i['adv']['minSingleTransAmount']
        tradableQuantity = i['adv']['tradableQuantity']
        monthOrderCount = i['advertiser']['monthOrderCount']
        monthFinishRate = i['advertiser']['monthFinishRate']
        userGrade = i['advertiser']['userGrade']
        price = float(i['adv']['price'])
        banks = [method['identifier'] for method in i['adv']['tradeMethods']]
        advs.append(Adv(minSingleTransAmount=minSingleTransAmount,
                        maxSingleTransAmount=maxSingleTransAmount,
                        tradableQuantity=tradableQuantity,
                        monthOrderCount=monthOrderCount,
                        monthFinishRate=monthFinishRate,
                        userGrade=userGrade,
                        price=price,
                        banks=banks,
                        ))
    return advs


def get_all_advs(asset, fiat, type):
    res = []
    page = 1
    if fiat == 'RUB':
        banks = ['Tinkoff']
    elif fiat in ['USD', 'EUR']:
        banks = ['KaspiBank', 'AltynBank']
    else:
        raise RuntimeError('err')
    while True:
        advs = get_page_advertisments(asset=asset, fiat=fiat, type=type, page=page, banks=banks)
        if advs:
            res.extend(advs)
            page += 1
        else:
            return res


def get_good_advs(advs, banks, min_monthOrderCount=50, min_monthFinishRate=0.95):
    return list(
        filter(
            lambda adv: adv.monthOrderCount > min_monthOrderCount and adv.monthFinishRate > min_monthFinishRate and set(
                adv.banks).intersection(banks),
            advs))


def get_best(advs, type):
    if not advs:
        return False
    res = list(sorted(advs, key=lambda adv: adv.price))
    if type == 'BUY':
        return res[0]
    elif type == 'SELL':
        return res[-1]
    else:
        raise Exception("invalid")


# RUB_USDT_EUR

def calc_price(fiat1, crypto, fiat2, comission=1.0):
    adv_buy_crypto = get_best(get_good_advs(get_all_advs(crypto, fiat1, 'BUY'), ['Tinkoff']), 'BUY')
    adv_sell_crypto = get_best(get_good_advs(get_all_advs(crypto, fiat2, 'SELL'), ['KaspiBank', 'AltynBank']), 'SELL')
    if adv_buy_crypto and adv_sell_crypto:
        # print(adv_buy_crypto)
        # print(adv_sell_crypto)
        return (adv_buy_crypto.price / adv_sell_crypto.price) * comission
    else:
        return None


print('real' + '-' * 20)
url = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(url)
print(converter.convert('EUR', 'RUB', 1))

print('direct' + '-' * 20)
# to euro
for crypto in COINS_BINANCE:
    print(crypto)
    price = calc_price('RUB', crypto, 'EUR')
    if price:
        print(price)
    else:
        print("Not available")

print('throw usd' + '-' * 20)
# to dollars and after to eur
for crypto in COINS_BINANCE:
    print(crypto)
    price = calc_price('RUB', crypto, 'EUR', comission=FF_DOLLARS_IN_EURO)
    if price:
        print(price)
    else:
        print("Not available")
