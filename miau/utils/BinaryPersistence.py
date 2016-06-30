import pickle   # Python object serialization

class BinaryPersistence(Persistence):
    def __init__(self, data_filepath):
        self.data_filepath = data_filepath

    def save(self, data):
        with open(self.data_filepath, 'wb') as file:
            pickle.dump(data, file)

    def load(self):
        try:
            with open(self.data_filepath, 'rb') as file:
                data = pickle.load(file)
        except EOFError:
            data = None
        return data
