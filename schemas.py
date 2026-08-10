from pydantic import BaseModel, Field
from typing import Optional, Any

class PhoneCreate(BaseModel):
    phone_code: str = Field(..., min_length=4, max_length=10)
    price: float = Field(..., gt=0)
    brand_id: int

class BrandResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PhoneResponse(BaseModel):
    id: int
    phone_code: str
    price: float
    brand: BrandResponse

    class Config:
        from_attributes = True

class StandardResponse(BaseModel):
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[Any] = None