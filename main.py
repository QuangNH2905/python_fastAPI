from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

uri = "mongodb+srv://quangnh:Nguthisong123@pythoncluster.0rxopzz.mongodb.net/?retryWrites=true&w=majority&appName=pythonCluster"
# Create a new client and connect to the server
client = AsyncIOMotorClient(uri)
db = client["student"]          # database tên student
collection = db["student_management"]       # collection tên studen_management

app = FastAPI()
origins = [
    "http://localhost:3000",  # hoặc domain frontend thật sự
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # KHÔNG dùng ["*"] nếu allow_credentials=True
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



class Student(BaseModel):
    mssv: str
    name: str
    email: str
    dob: str  # Date of Birth
    address: str
    diemToan: float
    diemVan: float
    diemAnh: float
# Database giả (dùng dictionary)
students_db = {}
# CREATE
@app.post("/students/")
async def create_student(student: Student):
    existing = await collection.find_one({"mssv": student.mssv})
    if existing:
        raise HTTPException(status_code=400, detail="Item already exists")
    result = await collection.insert_one(student.model_dump())
    return {"message": "Item created", "id": str(result.inserted_id)}


# READ (tất cả)
@app.get("/students/")
async def read_students():
    students = await collection.find().to_list(100)
    return [student_serializer(student) for student in students]

def student_serializer(student):
    student["_id"] = str(student["_id"])
    return student