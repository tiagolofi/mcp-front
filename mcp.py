
import requests
import json
from typing import List, Dict, Any

class Mcp:

    def login(data: Dict[str, str]):
        return requests.post("https://mcp-server-client-4dc341cd8433.herokuapp.com/login", json = data, timeout = 5).text.strip()

    def get_tools(token: str) -> List[Dict[str, Any]]:
        return requests.get(
            url = "https://mcp-server-client-4dc341cd8433.herokuapp.com/mcp/tools",
            headers = {
                'Authorization': f'Bearer {token}'
            }
        ).json()

    def post_mcp(tool_id: int, token: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return requests.post(
            f"https://mcp-server-client-4dc341cd8433.herokuapp.com/mcp?toolId={tool_id}", 
            json = data, 
            headers = {
                'Authorization': f'Bearer {token}'
            }
        ).json()

    def to_string(data: List[Dict[str, Any]]) -> str:
        return json.dumps(data, indent = 2, ensure_ascii = False)

    
