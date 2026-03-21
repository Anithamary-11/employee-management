from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import mysql.connector

from backend.db import get_db_connection
from backend.models import PayrollCreate
from backend.utils.salary_calculator import calculate_salary_components

router = APIRouter(prefix="/api/payroll", tags=["Payroll"])

@router.get("/", response_model=dict)
def get_payroll_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=1000),
    emp_id: Optional[int] = None,
    search: Optional[str] = None,
    sort_by: str = Query("payroll_id"),
    order: str = Query("desc")
):
    offset = (page - 1) * limit
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT p.*, e.name as employee_name, e.department, e.designation 
            FROM payroll p
            JOIN employees e ON p.emp_id = e.emp_id
        """
        count_query = "SELECT COUNT(*) as total FROM payroll p JOIN employees e ON p.emp_id = e.emp_id"
        params = []
        conditions = []
        
        if emp_id:
            conditions.append("p.emp_id = %s")
            params.append(emp_id)
        if search:
            conditions.append("(e.name LIKE %s OR e.department LIKE %s)")
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
            
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
            query += where_clause
            count_query += where_clause
            
        valid_sort_fields = ["payroll_id", "employee_name", "salary_date", "basic_salary", "net_salary"]
        actual_sort_by = sort_by if sort_by in valid_sort_fields else "payroll_id"
        if actual_sort_by == "employee_name":
            actual_sort_by = "e.name"
        else:
            actual_sort_by = "p." + actual_sort_by
        actual_order = "ASC" if order.lower() == "asc" else "DESC"
        
        query += f" ORDER BY {actual_sort_by} {actual_order} LIMIT %s OFFSET %s"
        
        cursor.execute(count_query, params)
        total_records = cursor.fetchone()['total']
        
        params.extend([limit, offset])
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        return {
            "data": records,
            "total": total_records,
            "page": page,
            "limit": limit
        }
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()

@router.get("/{payroll_id}", response_model=dict)
def get_payroll_slip(payroll_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT p.*, e.name, e.department, e.designation, e.email, e.doj
            FROM payroll p
            JOIN employees e ON p.emp_id = e.emp_id
            WHERE p.payroll_id = %s
        """
        cursor.execute(query, (payroll_id,))
        record = cursor.fetchone()
        if not record:
            raise HTTPException(status_code=404, detail="Payroll record not found")
        return record
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=dict)
def add_salary(payroll: PayrollCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT emp_id FROM employees WHERE emp_id = %s", (payroll.emp_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Employee not found")
            
        components = calculate_salary_components(payroll.basic_salary, payroll.bonus)
        
        query = """
            INSERT INTO payroll 
            (emp_id, basic_salary, hra, da, pf, bonus, net_salary, salary_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            payroll.emp_id,
            payroll.basic_salary,
            components['hra'],
            components['da'],
            components['pf'],
            payroll.bonus,
            components['net_salary'],
            payroll.salary_date
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        return {
            "message": "Salary added successfully", 
            "payroll_id": cursor.lastrowid,
            "components": components
        }
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()
