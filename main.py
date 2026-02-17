from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import models, database, os

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

class PartItem(BaseModel):
    name: str
    qty: float
    price: float
    amount: float

class RecordSchema(BaseModel):
    id: str
    date: Optional[str] = ""
    duedate: Optional[str] = ""
    status: Optional[str] = "대기"
    name: str
    phone: str
    email: Optional[str] = ""
    carmodel: str
    plate: str
    year: Optional[str] = ""
    mileage: Optional[str] = ""
    color: Optional[str] = ""
    vin: Optional[str] = ""
    work: Optional[str] = ""
    tech: Optional[str] = ""
    parts: Optional[List[PartItem]] = []
    total: Optional[float] = 0
    pay: Optional[str] = "카드"
    paystatus: Optional[str] = "미결제"
    memo: Optional[str] = ""

    class Config:
        from_attributes = True

@app.get("/records")
def get_records(db: Session = Depends(database.get_db)):
    return db.query(models.Record).order_by(models.Record.created_at.desc()).all()

@app.post("/records")
def create_record(record: RecordSchema, db: Session = Depends(database.get_db)):
    existing = db.query(models.Record).filter(models.Record.id == record.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다")
    parts_data = [p.dict() for p in record.parts] if record.parts else []
    db_record = models.Record(**record.dict(exclude={"parts"}), parts=parts_data)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.put("/records/{record_id}")
def update_record(record_id: str, record: RecordSchema, db: Session = Depends(database.get_db)):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")
    parts_data = [p.dict() for p in record.parts] if record.parts else []
    for key, value in record.dict(exclude={"parts"}).items():
        setattr(db_record, key, value)
    db_record.parts = parts_data
    db.commit()
    db.refresh(db_record)
    return db_record

@app.delete("/records/{record_id}")
def delete_record(record_id: str, db: Session = Depends(database.get_db)):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")
    db.delete(db_record)
    db.commit()
    return {"message": "삭제완료"}
