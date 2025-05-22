from dataclasses import dataclass

#Product Modal
@dataclass
class Product:
    name: str
    description:str
    price:float
    quantity: int

