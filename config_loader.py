import json
import os

class Config:
    def __init__(self, path='config/config.json'):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        with open(self.path) as f:
            self.settings = json.load(f)
    def get(self, key, default=None):
        return self.settings.get(key, default)
