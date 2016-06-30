import pickle   # Python object serialization

class BinaryPersistence(Persistence):

    def __init__(self, dataFilepath):
        super()
        self.__dataFilepath = dataFilepath

    def _loadData(self):
        try:
            with open(self.__dataFilepath, 'rb') as file:
                data = pickle.load(file)
        except EOFError:
            data = []
        return data

    def _saveData(self):
        with open(self.__dataFilepath, 'wb') as file:
            pickle.dump(self.getData(), file)

    def save(self, element):
        self.getData().append(element)
        self._saveData()

    def delete(self, element):
        if element in self.getData():
            self.getData().remove(element)
            self._saveData()

    def deleteAll(self, element):
        while element in self.getData():
            self.getData().remove(element)
        self._saveData()

    def clearData(self):
        super().clearData()
        self._saveData()
