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

@app.get("/students")
def get_students(db: Session = Depends(get_db)):

    students = db.query(models.Student).all()

    result = [
        {
            "id": s.id,
            "name": s.name,
            "course": s.course,
            "city": s.city
        }
        for s in students
    ]

    return result

@app.get("/")
def home():
    return {"message": "Fastapi working successfully."}