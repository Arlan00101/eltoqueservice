import requests
from typing import Optional, Dict, Any, List
from app.config import Config


class ElToqueClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.ELTOQUE_API_KEY
        self.base_url = Config.ELTOQUE_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_tasas_informales(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/tasas/informal"
        response = requests.get(endpoint, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_tasas_oficiales(self) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/tasas/oficial"
        response = requests.get(endpoint, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_tasas_historico(
        self, fecha_inicio: str, fecha_fin: str, tipo: str = "informal"
    ) -> List[Dict[str, Any]]:
        endpoint = f"{self.base_url}/tasas/historico"
        params = {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "tipo": tipo}
        response = requests.get(
            endpoint, headers=self.headers, params=params, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_all_tasas(self) -> Dict[str, Any]:
        return {
            "informal": self.get_tasas_informales(),
            "oficial": self.get_tasas_oficiales(),
        }
