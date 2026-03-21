from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import mysql.connector

from backend.db import get_db_connection
from backend.models import EmployeeCreate, EmployeeUpdate, EmployeeOut

router = APIRouter(prefix="/api/employees", tags=["Employees"])

@router.get("/", response_model=dict)
def get_employees(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=1000),
    search: Optional[str] = None,
    sort_by: str = Query("emp_id"),
    order: str = Query("desc")
):
    offset = (page - 1) * limit
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM employees"
        count_query = "SELECT COUNT(*) as total FROM employees"
        params = []
        
        if search:
            query += " WHERE name LIKE %s OR email LIKE %s OR department LIKE %s"
            count_query += " WHERE name LIKE %s OR email LIKE %s OR department LIKE %s"
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])
            
        valid_sort_fields = ["emp_id", "name", "email", "department", "designation"]
        actual_sort_by = sort_by if sort_by in valid_sort_fields else "emp_id"
        actual_order = "ASC" if order.lower() == "asc" else "DESC"
        
        query += f" ORDER BY {actual_sort_by} {actual_order} LIMIT %s OFFSET %s"
        
        cursor.execute(count_query, params)
        total_records = cursor.fetchone()['total']
        
        params.extend([limit, offset])
        cursor.execute(query, params)
        employees = cursor.fetchall()
        
        return {
            "data": employees,
            "total": total_records,
            "page": page,
            "limit": limit
        }
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()

@router.get("/{emp_id}", response_model=EmployeeOut)
def get_employee(emp_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
        emp = cursor.fetchone()
        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")
        return emp
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=dict)
def create_employee(emp: EmployeeCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO employees (name, gender, phone, email, designation, department, doj)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (emp.name, emp.gender.value, emp.phone, emp.email, emp.designation, emp.department, emp.doj)
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Employee created successfully", "emp_id": cursor.lastrowid}
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()

@router.put("/{emp_id}")
def update_employee(emp_id: int, emp: EmployeeUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        update_fields = []
        values = []
        for field, value in emp.model_dump(exclude_unset=True).items():
            if value is not None:
                if field == "gender":
                    update_fields.append(f"{field} = %s")
                    values.append(value.value)
                else:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
                    
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
            
        update_str = ", ".join(update_fields)
        query = f"UPDATE employees SET {update_str} WHERE emp_id = %s"
        values.append(emp_id)
        
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found or no changes made")
            
        return {"message": "Employee updated successfully"}
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()

@router.delete("/{emp_id}")
def delete_employee(emp_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"message": "Employee deleted successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()
