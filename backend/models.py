from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from enum import Enum

class GenderEnum(str, Enum):
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'

class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    gender: GenderEnum
    phone: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    designation: str = Field(..., min_length=2, max_length=100)
    department: str = Field(..., min_length=2, max_length=100)
    doj: date

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    designation: Optional[str] = Field(None, min_length=2, max_length=100)
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    doj: Optional[date] = None

class EmployeeOut(EmployeeCreate):
    emp_id: int

class PayrollCreate(BaseModel):
    emp_id: int
    basic_salary: float = Field(..., gt=0)
    bonus: float = Field(0.00, ge=0)
    salary_date: date

class PayrollOut(PayrollCreate):
    payroll_id: int
    hra: float
    da: float
    pf: float
    net_salary: float
