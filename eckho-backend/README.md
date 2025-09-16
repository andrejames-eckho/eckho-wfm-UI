# Eckho WFM Backend

A FastAPI backend for the Eckho Workforce Management system.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Documentation

Once running, visit:
- API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Features

- **Authentication**: JWT-based auth for admin and employee users
- **Time Tracking**: Clock in/out, break management
- **Employee Management**: CRUD operations for employee data
- **Historical Records**: Generate and retrieve time tracking history
- **Dashboard Analytics**: Summary statistics and reports

## Default Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Employees
All employees use password: `emp123`
- john.smith, sarah.johnson, mike.davis, emily.wilson, david.brown, lisa.anderson
- ava.martinez, noah.clark, mia.lee, ethan.hernandez, isabella.walker

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login

### Employees
- `GET /api/employees` - Get all employees (admin only)
- `GET /api/employees/{id}` - Get specific employee
- `PUT /api/employees/{id}/status` - Update employee status (admin only)

### Time Tracking
- `POST /api/time-tracking` - Clock in/out, break actions
- `GET /api/time-tracking/{id}` - Get current tracking status
- `GET /api/time-records/{id}` - Get historical records

### Dashboard
- `GET /api/dashboard/summary` - Get dashboard statistics (admin only)
- `POST /api/employees/date-records` - Get employees for specific date (admin only)

## Data Models

The backend includes comprehensive data models for:
- User authentication and roles
- Employee information (warehouse and field employees)
- Time tracking data
- Historical records
- Status management

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`
