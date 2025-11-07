
import requests
import json
from typing import List, Dict, Any, overload
from dotenv import load_dotenv
from os import getenv

load_dotenv(override=True)

MCP_USERNAME = getenv('MCP_USERNAME')
MCP_PASSWORD = getenv('MCP_PASSWORD')

class Mcp:

    _instance = None

    def __init__(self) -> None:
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @overload
    def login(self, data: None) -> str: ...

    def login(self, data: Dict[str, str] = None) -> str:
        if data is None:
            data = {'username': MCP_USERNAME, 'password': MCP_PASSWORD}
        return requests.post("https://mcp-server-client-4dc341cd8433.herokuapp.com/login", json = data, timeout = 5).text.strip()

    def get_tools(self, token: str) -> List[Dict[str, Any]]:
        return requests.get(
            url = "https://mcp-server-client-4dc341cd8433.herokuapp.com/mcp/tools",
            headers = {
                'Authorization': f'Bearer {token}'
            }
        ).json()

    def post_mcp(self, tool_id: int, token: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return requests.post(
            f"https://mcp-server-client-4dc341cd8433.herokuapp.com/mcp?toolId={tool_id}", 
            json = data, 
            headers = {
                'Authorization': f'Bearer {token}'
            }
        ).json()

    def to_string(self, data: List[Dict[str, Any]]) -> str:
        return json.dumps(data, indent = 2, ensure_ascii = False)

    
