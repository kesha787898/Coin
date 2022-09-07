import json

import requests

from Order import Order
from BaseCollector import BaseCollector


class APICollector(BaseCollector):

    @staticmethod
    def get_page_advertisments(asset, fiat, type, banks, page=0):
        data = {
            "asset": asset,
            "countries": [],
            "fiat": fiat,
            "page": page,
            "payTypes": banks,
            "proMerchantAds": False,
            "publisherType": None,
            "rows": 10,
            "tradeType": type,
        }
        response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', json=data)
        resp_data = json.loads(response.text)['data']
        advs = []
        if not resp_data:
            return advs
        for i in resp_data:
            price = float(i['adv']['price'])
            tradable_quantity = i['adv']['tradableQuantity']
            adv = Order(price=price, asset=asset, fiat=fiat, type=type, tradable_quantity=tradable_quantity)
            advs.append(adv)
        return advs

    @staticmethod
    def get_all_advs(asset, fiat, type, banks=None):
        res = []
        page = 1
        if not banks:
            if fiat == 'RUB':
                banks = ['TinkoffNew']
            elif fiat in ['USD', 'EUR']:
                banks = ['KaspiBank', 'AltynBank']
            else:
                raise RuntimeError('err')
        while True:
            advs = APICollector.get_page_advertisments(asset=asset, fiat=fiat, type=type, page=page, banks=banks)
            if advs:
                res.extend(advs)
                page += 1
            else:
                return res
