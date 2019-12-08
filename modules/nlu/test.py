import json

from utils import projpath

if __name__ == "__main__":
    train_data = json.load(projpath("resources/intents.json"))
    print(train_data)