from abc import ABC, abstractmethod
from ..repository.models import ProductCategory
import re
from .exceptions import (
    DuplicateNameError,
    InvalidFormatError,
    PriceOutOfRangeError,
    ForbiddenWordError,
)

class Specification(ABC):

    @abstractmethod
    def is_satisfied(self) -> bool:
        pass

    @abstractmethod
    def error_message(self) -> str:
        pass

    def and_(self, other: 'Specification') -> 'Specification':
        return AndSpecification(self, other)


class AndSpecification(Specification):

    def __init__(self, spec1: Specification, spec2: Specification):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied(self) -> bool:
        return self.spec1.is_satisfied() and self.spec2.is_satisfied(

        )

    def error_message(self) -> str:
        if not self.spec1.is_satisfied():
            return self.spec1.error_message()
        return self.spec2.error_message()


class NameFormatSpec(Specification):

    def __init__(self, name: str):
        self.name = name

    def is_satisfied(self) -> bool:
        if not re.match(r'^[a-zA-Z0-9]{3,20}$', self.name):
            raise InvalidFormatError(self.error_message())
        return True

    def error_message(self) -> str:
        return f'Pole name: Nazwa musi mieć 3-20 znaków i zawierać tylko litery i cyfry'


class NameUniquenessSpec(Specification):

    def __init__(self, name: str, existing_names: list, exclude_id: int = None):
        self.name = name.lower()
        self.existing_names = [n.lower() for n in existing_names]
        self.exclude_id = exclude_id

    def is_satisfied(self) -> bool:
        if self.name in self.existing_names:
            raise DuplicateNameError(self.error_message())
        return True

    def error_message(self) -> str:
        return f'Pole name: Produkt o nazwie {self.name} już istnieje'


class ForbiddenWordsSpec(Specification):

    def __init__(self, name: str, forbidden_words: list):
        self.name = name.lower()
        self.forbidden_words = forbidden_words
        self.found_word = None

    def is_satisfied(self) -> bool:
        for word in self.forbidden_words:
            if word == self.name:
                self.found_word = word
                raise ForbiddenWordError(self.error_message())
        return True

    def error_message(self) -> str:
        return f'Pole name: Nazwa zawiera zabronioną frazę: {self.found_word}'


class PriceRangeSpec(Specification):

    RANGES = {
        ProductCategory.ELECTRONICS: (50, 50000),
        ProductCategory.BOOKS: (5, 500),
        ProductCategory.CLOTHING: (10, 5000)
    }

    def __init__(self, price: float, category: ProductCategory):
        self.price = price
        self.category = category
        self.min, self.max = self.RANGES[category]

    def is_satisfied(self) -> bool:
        if not (self.min <= self.price <= self.max):
            raise PriceOutOfRangeError(self.error_message())
        return True

    def error_message(self) -> str:
        return f'Pole price: Cena {self.price} PLN poza zakresem {self.min}-{self.max} PLN dla kategorii {self.category.value}'


class ProductValidator:


    def __init__(self, repository, forbidden_word_repo):
        self.repo = repository
        self.forbidden_repo = forbidden_word_repo


    def validate(self, product_data, exclude_id: int = None):

        all_products = self.repo.get_all()
        print('Exclude id:', exclude_id)
        existing_names = [p.name for p in all_products if  exclude_id is None or p.id != exclude_id]
        forbidden_words = self.forbidden_repo.get_all_words()

        combined_spec = NameFormatSpec(product_data.name) \
            .and_(ForbiddenWordsSpec(product_data.name, forbidden_words)) \
            .and_(NameUniquenessSpec(product_data.name, existing_names, exclude_id)) \
            .and_(PriceRangeSpec(product_data.price, product_data.category))

        combined_spec.is_satisfied()
