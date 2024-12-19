# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Create the FastAPI instance
app = FastAPI()

# In-memory data store (using a dictionary to simulate a database)
employees_db = {}

# Pydantic model for request/response validation
class Employee(BaseModel):
    id: int
    name: str
    department: str

# 1. Create (POST) an Employee
@app.post("/employees/", response_model=Employee)
async def create_employee(item: Employee):
    item_id = len(employees_db) + 1
    employees_db[item_id] = item
    return item

# 2. Read (GET) an Employee by its ID
@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees_db[employee_id]

# 3. Update (PUT) an existing Employee by its ID
@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee: Employee):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    employees_db[employee_id] = employee
    return employee

# 4. Delete (DELETE) an Employee by its ID
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees_db[employee_id]
    return {"message": "Employee deleted successfully"}

# 5. List all Employees (GET)
@app.get("/employees/", response_model=List[Employee])
async def list_employees():
    return list(employees_db.values())
