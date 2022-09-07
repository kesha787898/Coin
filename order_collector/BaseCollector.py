from abc import ABC, abstractmethod


class BaseCollector(ABC):
    @staticmethod
    @abstractmethod
    def get_all_advs(asset, fiat, type, banks=None):
        pass
