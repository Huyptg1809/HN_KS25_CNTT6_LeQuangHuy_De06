from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    phones = relationship("Phone", back_populates="brand")

class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_code = Column(String(10), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    brand = relationship("Brand", back_populates="phones")