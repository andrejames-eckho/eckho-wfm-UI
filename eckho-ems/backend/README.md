ECKHO EMS Backend (FastAPI + PostgreSQL)

Setup

1. Python env
   - macOS:
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt

2. Environment
   - Copy ENV.example to .env and edit values
     cp ENV.example .env

3. Database
   - Ensure PostgreSQL is running and the database exists (e.g., eckho_ems)

4. Run
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

API

- GET /employees
- POST /employees
- GET /employees/{id}
- GET /time-records?employee_id=&start_date=&end_date=
- POST /time-records

CORS is open for development; restrict in production.

