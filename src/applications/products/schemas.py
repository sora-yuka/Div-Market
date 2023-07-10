from pydantic import BaseModel
from datetime import datetime


class ProductCreate(BaseModel):
    title: str
    owner: str
    description: str = None
    price: float = 0
    category: int
    created_at: datetime = datetime.utcnow()
    
    
class ProductEdit(BaseModel):
    id: int
    title: str
    description: str
    price: float = 0