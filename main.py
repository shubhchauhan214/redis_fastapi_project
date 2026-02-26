from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from schemas import StudentCreate

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/students")
def create_student(student: StudentCreate, db: Session=Depends(get_db)):
    new_student=models.Student(name=student.name, course=student.course, city=student.city)

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return{
        "message":"Student Created Successfully",
        "student_id": new_student.id
    }

@app.get("/")
def home():
    return {"message": "Fastapi working successfully."}