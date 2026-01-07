import requests
from typing import Optional, Dict, Any
from ...application.interfaces.product_service import IProductService

class HttpProductService(IProductService):
    def __init__(self, product_service_url: str):
        self.base_url = product_service_url.rstrip("/")

    def get_product_info(self, product_id: int) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(f"{self.base_url}/api/v1/products/{product_id}", timeout=4)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    def exists(self, product_id: int) -> bool:
        return self.get_product_info(product_id) is not None