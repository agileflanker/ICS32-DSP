from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, id: str, price: float):
        self.item_id = id
        self.price = price
    
    @abstractmethod
    def calculate_total_price(self, quantity: int):


class Regularitem(Item):
    def __init__(self, id: str, price: float):
        super().__init__(id, price)
    
    

def count_even(num: int) -> int:
    if num == 0:
        return 0
    else:
        if num % 2 == 0:
            return 1 + count_even(num//10)
        else:
            return count_even(num//10)

print(count_even(4343482287))