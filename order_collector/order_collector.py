import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import schedule
import logging
from config import is_stable, dump_frequency_sec
from APICollector import APICollector
from consts import Base
import config


def get_all_advs(asset_list, fiats_list, types):
    # Todo multithreading
    res = []
    for asset in asset_list:
        for fiat in fiats_list:
            for type in types:
                res.extend(APICollector.get_all_advs(asset, fiat, type))
    return res


def dump(engine):
    with Session(engine) as session:
        logging.debug("Start committing to DB")
        all_advs = get_all_advs(config.asset_list, config.fiats_list, config.types)
        print(len(all_advs))
        logging.debug(f"adding {all_advs} advs")
        session.add_all(all_advs)
        session.commit()
        logging.debug("Commited to DB")


#def dump(engine):
#    with Session(engine) as session:
#        logging.debug("Start committing to DB")
#
#        all_advs = APICollector.get_all_advs("USDT", "RUB", 'BUY')
#        print(len(all_advs))
#        logging.debug(f"adding {all_advs} advs")
#        session.add_all(all_advs)
#        session.commit()
#        logging.debug("Commited to DB")


def run():
    engine = create_engine(os.environ.get("BD_CONNECTION"),
                           echo=True, future=True)
    if not is_stable:
        logging.debug("Dropping DB")
        Base.metadata.drop_all(engine)
        logging.debug("Databases DB")

    logging.debug("Creating DB")
    Base.metadata.create_all(engine, checkfirst=True)
    logging.debug("Database DB")
    schedule.every(dump_frequency_sec).seconds.do(dump, engine=engine)
    while True:
        schedule.run_pending()


run()
