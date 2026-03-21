from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.routes import employee, payroll, dashboard

app = FastAPI(title="Employee Payroll Management API")

# Setup CORS to allow cross-origin requests from frontend (if separated)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee.router)
app.include_router(payroll.router)
app.include_router(dashboard.router)

# To serve frontend logic directly within FastAPI if desired
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
