
import json
from typing import Dict, Any

PATH_FILE = 'files.json'

class Cache:

    def __init__(self) -> None:
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __read(self) -> Dict[str, Any]:
        with open(PATH_FILE, 'r') as file:
            data = json.load(file)  
            return data
        
    def __write(self, data: Dict[str, Any]) -> None:
        with open(PATH_FILE, 'w') as file:
            json.dump(data, file, indent = 2)

    def get(self, id: str):
        data = self.__read()
        return data.get(id)

    def add(self, set: Dict[str, Any]) -> bool:
        try:
            data = self.__read()
            data.update(set)
            self.__write(data)
            return True
        except Exception:
            return False
        
    def update(self, id: str, set: Dict[str, Any]):
        try:
            data = self.__read()
            data[id] = set
            self.__write(data)
            return True
        except Exception:
            return False

    def remove(self, id: str):
        try:
            data = self.__read()
            data.pop(id)
            self.__write(data)
            return True
        except Exception:
            return False