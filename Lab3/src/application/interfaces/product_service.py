from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, Dict, Any


class IProductService(ABC):
    @abstractmethod
    def get_product_info(self, product_id: UUID) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def exists(self, product_id: UUID) -> bool:
        pass