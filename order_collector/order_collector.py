import json
import os
from datetime import datetime
from multiprocessing import Process

import requests
from flask import Flask
from sqlalchemy import Column, DateTime, String
from sqlalchemy import Integer, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import schedule
import logging
from config import is_stable, dump_frequency_sec

engine = create_engine(os.environ.get("BD_CONNECTION"), echo=True, future=True)

Base = declarative_base()


# Todo можно использовать только значения из списка.Подумать как сделать
class Order(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    price = Column(Float, primary_key=False)
    tradable_quantity = Column(Float, primary_key=False)
    asset = Column(String, primary_key=False)
    fiat = Column(String, primary_key=False)
    type = Column(String, primary_key=False)


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
        price = float(i['adv']['price'])
        tradable_quantity = i['adv']['tradableQuantity']
        adv = Order(price=price, asset=asset, fiat=fiat, type=type, tradable_quantity=tradable_quantity)
        advs.append(adv)
    return advs


def get_all_advs(asset, fiat, type, banks=None):
    res = []
    page = 1
    if not banks:
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


def dump():
    with Session(engine) as session:
        logging.debug("Start committing to DB")

        all_advs = get_all_advs("USDT", "RUB", 'BUY')
        logging.debug(f"adding {all_advs} advs")
        session.add_all(all_advs)
        session.commit()
        logging.debug("Commited to DB")


def run():
    if not is_stable:
        logging.debug("Dropping DB")
        Base.metadata.drop_all(engine)
        logging.debug("Databases DB")

    logging.debug("Creating DB")
    Base.metadata.create_all(engine, checkfirst=True)
    logging.debug("Database DB")
    schedule.every(dump_frequency_sec).seconds.do(dump)
    while True:
        schedule.run_pending()


server = Flask(__name__)


@server.route("/")
def health_check():
    return "started"


if __name__ == "__main__":
    p = Process(target=run)
    p.start()
    port = int(os.environ.get('PORT', 8050))
    server.run(host='0.0.0.0', port=port)
