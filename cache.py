
import json
from typing import Dict, Any

PATH_FILE = 'files.json'

class Cache:

    def insert(set: Dict[str, Any]) -> bool:
        try:
            with open(PATH_FILE, 'r') as file:
                data = json.load(file)

            data.update(set)

            with open(PATH_FILE, 'w') as file:
                json.dump(data, file, indent = 2)

            return True
        except Exception:
            return False
