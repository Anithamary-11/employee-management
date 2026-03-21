from fastapi import APIRouter, HTTPException
from backend.db import get_db_connection
import mysql.connector

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) as total_employees FROM employees")
        total_employees = cursor.fetchone()['total_employees']
        
        cursor.execute("SELECT COALESCE(SUM(net_salary), 0) as total_payroll FROM payroll")
        total_payroll = cursor.fetchone()['total_payroll']
        
        return {
            "total_employees": total_employees,
            "total_payroll": float(total_payroll)
        }
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()
