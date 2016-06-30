from abc import ABC, abstractmethod

class Persistence(ABC):

    def __init__(self):
        self.__data = _loadData()

    def getData(self):
        return self.__data

    @abstractmethod
    def _loadData(self):
        pass

    @abstractmethod
    def save(self, element):
        pass

    @abstractmethod
    def delete(self, element):
        pass

    @abstractmethod
    def deleteAll(self, element):
        pass

    def clearData(self):
        self.__data = []
