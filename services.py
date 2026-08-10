from sqlalchemy.orm import Session
import models
import schemas

def get_all_phones_service(db: Session):
    return db.query(models.Phone).all()

def check_brand_exists_service(db: Session, brand_id: int):
    return db.query(models.Brand).filter(models.Brand.id == brand_id).first()

def check_phone_code_exists_service(db: Session, phone_code: str):
    return db.query(models.Phone).filter(models.Phone.phone_code == phone_code).first()

def create_phone_service(db: Session, phone: schemas.PhoneCreate):
    new_phone = models.Phone(phone_code=phone.phone_code, price=phone.price, brand_id=phone.brand_id)
    db.add(new_phone)
    db.commit()
    db.refresh(new_phone)
    return new_phone

def get_brand_by_id_service(db: Session, brand_id: int):
    return db.query(models.Brand).filter(models.Brand.id == brand_id).first()

def delete_brand_service(db: Session, brand: models.Brand):
    db.delete(brand)
    db.commit()
    return brand