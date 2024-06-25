from pydantic import BaseModel

class ClothUnit(BaseModel):
    product_url: str
    sku: str
    product_name: str
    images: list[str]
    metadata: list[str]
    price: str
    sizes: list[str]
    cloth_type: str
