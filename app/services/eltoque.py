import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any
from app.config import Config
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ElToqueClient:
    def __init__(self):
        self.base_url = Config.ELTOQUE_API_URL
        self.api_key = Config.ELTOQUE_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)

    def get_trmi(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/v1/trmi"
        response = self.session.get(endpoint, headers=self.headers, timeout=30, verify=False)
        response.raise_for_status()
        return response.json()