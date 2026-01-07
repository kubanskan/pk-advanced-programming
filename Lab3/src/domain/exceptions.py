class DomainException(Exception):
    pass

class CartNotFoundException(DomainException):
    def __init__(self, cart_id):
        super().__init__(f'Koszyk o ID {cart_id} nie został znaleziony.')

class ProductNotFoundException(DomainException):
    '''Rzucany, gdy produkt nie istnieje w zewnętrznym serwisie.'''
    pass

class EmptyCartException(DomainException):
    '''Rzucany przy próbie checkoutu pustego koszyka.'''
    pass