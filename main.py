from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session
import models, schemas, services
from database import engine, SessionLocal, get_db
from core import raw_phones, clean_and_validate_phones

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        valid_data = clean_and_validate_phones(raw_phones)
        for item in valid_data:
            brand = db.query(models.Brand).filter(models.Brand.name == item["brand"]).first()
            if not brand:
                brand = models.Brand(name=item["brand"])
                db.add(brand)
                db.commit()
                db.refresh(brand)
            
            phone = db.query(models.Phone).filter(models.Phone.phone_code == item["phone_code"]).first()
            if not phone:
                new_phone = models.Phone(
                    phone_code=item["phone_code"],
                    price=item["price"],
                    brand_id=brand.id
                )
                db.add(new_phone)
                db.commit()
    finally:
        db.close()

@app.get("/phones", response_model=schemas.StandardResponse)
def get_phones(response: Response, db: Session = Depends(get_db)):
    phones = services.get_all_phones_service(db)
    data_list = [schemas.PhoneResponse.model_validate(p) for p in phones]
    return schemas.StandardResponse(
        statusCode=200,
        error=None,
        message="Lấy danh sách điện thoại thành công",
        data=data_list
    )

@app.post("/phones", response_model=schemas.StandardResponse)
def create_phone(phone: schemas.PhoneCreate, response: Response, db: Session = Depends(get_db)):
    brand = services.check_brand_exists_service(db, phone.brand_id)
    if not brand:
        response.status_code = 404
        return schemas.StandardResponse(
            statusCode=404, error="Not Found", message="Hãng điện thoại không tồn tại", data=None
        )

    existing_phone = services.check_phone_code_exists_service(db, phone.phone_code)
    if existing_phone:
        response.status_code = 400
        return schemas.StandardResponse(
            statusCode=400, error="Bad Request", message="Mã điện thoại đã tồn tại", data=None
        )

    new_phone = services.create_phone_service(db, phone)
    
    return schemas.StandardResponse(
        statusCode=201, 
        error=None, 
        message="Thêm điện thoại thành công", 
        data=schemas.PhoneResponse.model_validate(new_phone)
    )

@app.delete("/brands/{id}", response_model=schemas.StandardResponse)
def delete_brand(id: int, response: Response, db: Session = Depends(get_db)):
    brand = services.get_brand_by_id_service(db, id)
    
    if not brand:
        response.status_code = 404
        return schemas.StandardResponse(
            statusCode=404, error="Not Found", message="Hãng điện thoại không tồn tại", data=None
        )
        
    if brand.phones:
        response.status_code = 400
        return schemas.StandardResponse(
            statusCode=400, 
            error="Bad Request", 
            message="Không thể xóa hãng vì vẫn còn điện thoại thuộc hãng này", 
            data=None
        )

    services.delete_brand_service(db, brand)
    
    return schemas.StandardResponse(
        statusCode=200, error=None, message="Xóa hãng thành công", data=None
    )