import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "employee_management")

try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        pool_reset_session=True,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print("Database connection pool initialized.")
except mysql.connector.Error as err:
    print(f"Error initializing connection pool: {err}")
    connection_pool = None

def get_db_connection():
    if not connection_pool:
        raise Exception("Database connection pool is not configured properly.")
    return connection_pool.get_connection()
