from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    name:str
    course:str
    city:str