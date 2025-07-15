import json
from behavior.settings import SAVE_DATA_PATH

class Data:
    def __init__(self):
        self.data = None
        self.load_data()
    
    def load_data(self):
        with open(SAVE_DATA_PATH, 'r') as openfile:
            self.data = json.load(openfile)

    def save_data(self, input_data:dict):
        new_data = self.data

        if self.data and input_data["score"] > self.data["high_score"]:
            new_data = self.data
            new_data["high_score"] = input_data["score"]

        if self.data and input_data["achievements"] != self.data["achievements"]:
            new_data["achievements"] = input_data["achievements"]

        #Write new data
        with open(SAVE_DATA_PATH, "w") as outfile:
            json.dump(new_data, outfile)
    
    def reset_data(self):
        new_data = {"high_score": 0, "achievements": []}

        #Write new data
        with open(SAVE_DATA_PATH, "w") as outfile:
            json.dump(new_data, outfile)