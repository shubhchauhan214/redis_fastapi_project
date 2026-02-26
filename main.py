from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from schemas import StudentCreate
from redis_client import redis_client
import json

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/students")
def create_student(student: StudentCreate, db: Session=Depends(get_db)):
    new_student=models.Student(name=student.name, course=student.course, city=student.city)

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    redis_client.delete("students_list")

    return{
        "message":"Student Created Successfully",
        "student_id": new_student.id
    }

@app.get("/students")
def get_students(db: Session = Depends(get_db)):

    #Check Cache
    cached_data = redis_client.get("students_list")

    if cached_data:
        print("From Redis")
        return json.loads(cached_data)
    
    print("From Database")

    # Fetch from DB
    students=db.query(models.Student).all()

    result = [
        {
            "id": s.id,
            "name":s.name,
            "course":s.course,
            "city":s.city
        }
        for s in students
    ]

    #Store in Redis
    redis_client.set("students_list", json.dumps(result), ex=60)

    return result

@app.get("/")
def home():
    return {"message": "Fastapi working successfully."}