# Employee Payroll Management System

A production-ready Employee Payroll Management System built with a Python FastAPI backend and a responsive Tabler.io frontend.

## 🌟 Features
- **Dashboard**: Quick summary of total employees and processed payroll values.
- **Employee Management**: Full CRUD (Create, Read, Update, Delete) capability with pagination, live search, and CSV export. Form elements have real-time validation.
- **Payroll Module**: Process employee salaries. Automatically calculates HRA (20%), DA (10%), PF (5%), and net salary. Includes a print-ready payslip view.

## 🛠️ Tech Stack
- **Backend / API**: Python 3, FastAPI, Pydantic
- **Database**: MySQL (with connection pooling via `mysql-connector-python`)
- **Frontend**: HTML5, Vanilla JavaScript, CSS, Tabler.io UI Framework

---

## 🚀 Step-by-Step Setup Guide

Follow these instructions to run the application locally.

### Step 1: Database Setup
1. Launch your MySQL server instance (e.g., using XAMPP, WAMP, or standalone MySQL).
2. Open your preferred database tool (e.g., phpMyAdmin or MySQL Workbench) or use the command line.
3. Import the database schema by executing the provided file:
   ```bash
   source database.sql
   ```
4. Optional: Populate the database with sample test data by executing:
   ```bash
   source sample_data.sql
   ```
*(Note: Ensure the database `employee_management` is actually visible inside your database gui.)*

### Step 2: Environment Configuration
1. In the root of the project, locate the `.env.example` file.
2. Copy it and rename it to exactly `.env`.
3. Open the `.env` file and update your MySQL credentials based on your database configuration:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=employee_management
   ```

### Step 3: Backend Setup
1. Open a terminal and navigate to your project directory.
2. Create a virtual environment to safely install python packages:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows**: `.\venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`
4. Install all backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the FastAPI application server:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
   *The backend should now be running. You can test the APIs in an auto-generated swagger UI at http://127.0.0.1:8000/docs.*

### Step 4: Frontend Execution
The frontend is written in pure browser-compatible code. The safest way to prevent CORS blockages around browser modules is to host it properly over an HTTP server.
1. Open a **new** terminal window and navigate to the project directory again:
   ```bash
   cd frontend
   ```
2. Start a simple Python web server to host the static HTML files:
   ```bash
   python -m http.server 3000
   ```
3. Open your web browser and visit:
   ```
   http://localhost:3000/dashboard.html
   ```

🎉 **You are all set!** Navigate between Dashboard, Employees, and Payroll modules natively.

---

## 🌍 Production Deployment

### 1. Backend (FastAPI + MySQL)
Netlify **only hosts static files** (HTML/JS/CSS), so your Python backend and MySQL Database must be hosted on a dynamic hosting provider (e.g., Render, Railway, or Heroku).
1. Deploy your FastAPI repository to Render or Railway.
2. In the provider's Dashboard, navigate to **Environment Variables**.
3. Add the exact keys from your `.env` file (e.g., `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) configuring them to match your production MySQL database server.

### 2. Frontend (Netlify)
Once your Python backend is live and exposes a public URL:
1. Open `frontend/assets/app.js` locally.
2. At the very top of the file, alter `API_BASE` to match your new production backend URL:
   ```javascript
   const API_BASE = 'https://your-production-app.onrender.com/api';
   ```
3. Create a free account on [Netlify](https://www.netlify.com/).
4. Navigate to **"Add new site"** -> **"Deploy manually"**.
5. Drag and drop your entire `frontend` folder directly into the Netlify deployment dropzone.
6. Your static dashboard will instantly go live and perfectly route all API queries directly to your hosted Python backend!
