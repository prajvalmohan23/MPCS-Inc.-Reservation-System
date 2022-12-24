import json

class UserDataManager:
    def __init__(self, user_file):
        self.user_file = user_file

    def load(self):
        with open(self.user_file) as uf:
            staff_data = json.load(uf)
        return staff_data

    def save(self, staff_data):
        with open(self.user_file, "w") as uf:
            json.dump(staff_data, uf)