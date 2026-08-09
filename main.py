from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import HTTPException
from typing import Optional

app = FastAPI()

student: list = []


class Student(BaseModel):
    name: str
    student_id: int
    branch: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    branch: Optional[str] = None


class ReplaceStudent(BaseModel):
    name: str
    branch: str


@app.post("/student", response_model=Student, tags=["Student"])
def student_data(students: Student):
    if students.student_id <= 0:
        raise HTTPException(status_code=400, detail="error : student id cannot be 0")
    for std in student:
        if students.student_id == std.student_id:
            raise HTTPException(status_code=409, detail="error : duplicate student id")
    if not students.name.strip():
        raise HTTPException(status_code=400, detail="empty name")
    if not students.branch.strip():
        raise HTTPException(status_code=400, detail="empty branch data")
    student.append(students)

    return students


@app.get("/student", response_model=list[Student], tags=["Student"])
def get_student():
    return student


@app.get("/student/search", response_model=list[Student], tags=["Student"])
def search_by_branch(branch: str):
    result: list = []
    for std in student:
        if std.branch.lower().strip() == branch.strip().lower():
            result.append(std)
    if not result:
        raise HTTPException(status_code=404, detail="student not found")
    else:
        return result


@app.get("/student/{id}", tags=["Student"])
def get_stud(id: int):
    for std in student:
        if std.student_id == id:
            return {"status": "student found", "student": std}
    raise HTTPException(status_code=404, detail="student not found")


@app.put("/student/{id}", response_model=Student, tags=["Student"])
def put_student(id: int, std: ReplaceStudent):
    for stud in student:
        if stud.student_id == id:
            stud.name = std.name
            stud.branch = std.branch
            return stud
    raise HTTPException(status_code=404, detail="student not found")


@app.patch("/student/{id}", response_model=Student, tags=["Student"])
def patch_student(id: int, stud: UpdateStudent):
    for std in student:
        if std.student_id == id:
            if stud.name is not None:
                if stud.name.strip() == "":
                    raise HTTPException(status_code=400, detail="name cannot be empty")
                std.name = stud.name
            if stud.branch is not None:
                if stud.branch.strip() == "":
                    raise HTTPException(
                        status_code=400, detail="branch cannot be empty"
                    )
                std.branch = stud.branch
            return std
    raise HTTPException(status_code=404, detail="student not found")


@app.delete("/student/{id}", tags=["Student"])
def delete_student(id: int):
    for stud in student:
        if stud.student_id == id:
            student.remove(stud)
            return {"status": "student delete successfully"}
    raise HTTPException(status_code=404, detail="student not found")
