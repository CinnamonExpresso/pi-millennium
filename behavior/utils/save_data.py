import json

class Data:
    def __init__(self):
        self.data = {}
        self.data_path = "data/save.json"
    
    def load_data(self):
        with open(self.data_path, 'r') as openfile:
            self.data = json.load(openfile)

    def save_score(self, score:int):
        if self.data and score > self.data["high_score"]:
            new_data = self.data
            new_data["high_score"] = score

            with open(self.data_path, "w") as outfile:
                json.dump(new_data, outfile)