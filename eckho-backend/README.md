# Eckho WFM Backend

A FastAPI-based backend for the Eckho Workforce Management System with PostgreSQL database integration.

## Features

- **Authentication System**: JWT-based authentication for admin and employee users
- **Employee Management**: CRUD operations for employee data
- **Time Tracking**: Clock in/out, break management, and overtime tracking
- **Dashboard Analytics**: Real-time employee status and summary statistics
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with passlib
- **Migration**: Alembic
- **Containerization**: Docker & Docker Compose

## Project Structure

```
eckho-backend/
├── app/                          # Main application package
│   ├── api/                      # API routes and endpoints
│   │   ├── __init__.py
│   │   └── main.py              # FastAPI app and route definitions
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   ├── db_models.py         # SQLAlchemy database models
│   │   └── models.py            # Pydantic request/response models
│   └── services/                 # Business logic and services
│       ├── __init__.py
│       ├── auth.py              # Authentication service
│       ├── database.py          # Database connection and session
│       └── db_service.py        # Database operations
├── alembic/                      # Database migrations
│   ├── versions/
│   └── env.py
├── scripts/                      # Utility scripts
│   ├── init_db.py              # Database initialization script
│   ├── init_db.sql             # SQL initialization script
│   └── start_db.sh             # Database startup script
├── config/                       # Configuration files (moved to root)
├── main.py                      # Application entry point
├── docker-compose.yml           # Docker services configuration
├── alembic.ini                  # Alembic configuration
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose
- PostgreSQL (or use Docker container)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd eckho-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start PostgreSQL database**
   ```bash
   docker-compose up -d
   ```

6. **Initialize database**
   ```bash
   python scripts/init_db.py
   ```

7. **Run the application**
   ```bash
   python main.py
   # or
   uvicorn app.api.main:app --host 0.0.0.0 --port 8001 --reload
   ```

## Database Setup

### Using Docker (Recommended)

The project includes a Docker Compose configuration for PostgreSQL:

```bash
# Start PostgreSQL container
docker-compose up -d

# Initialize database with dummy data
python scripts/init_db.py

# Stop container
docker-compose down
```

### Manual PostgreSQL Setup

If you prefer to use a local PostgreSQL installation:

1. Create database and user:
   ```sql
   CREATE USER eckho_user WITH PASSWORD 'eckho_password';
   CREATE DATABASE eckho_wfm OWNER eckho_user;
   GRANT ALL PRIVILEGES ON DATABASE eckho_wfm TO eckho_user;
   ```

2. Update `.env` file with your database credentials

3. Run database initialization:
   ```bash
   python scripts/init_db.py
   ```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

## API Endpoints

### Authentication
- `POST /api/auth/login` - Admin/Employee login

### Employee Management
- `GET /api/employees` - Get all employees
- `GET /api/employees/{id}` - Get employee by ID
- `PUT /api/employees/{id}/status` - Update employee status
- `POST /api/employees/date-records` - Get employees for specific date

### Time Tracking
- `POST /api/time-tracking` - Perform time tracking action
- `GET /api/time-tracking/{employee_id}` - Get current tracking status
- `GET /api/time-records/{employee_id}` - Get historical time records

### Dashboard
- `GET /api/dashboard/summary` - Get dashboard summary
- `GET /api/status-colors` - Get status color mappings

## Database Schema

### Tables

1. **admins**
   - id, username, password_hash, created_at

2. **employees**
   - id, first_name, last_name, employee_type, expected_start_time, created_at

3. **current_time_tracking**
   - id, employee_id, current_status, time_in, time_out, break_in, break_out, date

4. **time_records**
   - id, employee_id, date, time_in, time_out, break_in, break_out, total_hours, status

## Default Credentials

### Admin Account
- Username: `admin`
- Password: `admin123`

### Employee Accounts
- Username: Employee ID (1-11)
- Password: `emp123`

## Environment Variables

```env
# Database Configuration
DATABASE_URL=postgresql://eckho_user:eckho_password@127.0.0.1:5432/eckho_wfm

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development

```bash
# Start database
docker-compose up -d

# Stop database
docker-compose down

# View logs
docker-compose logs

# Reset database (removes all data)
docker-compose down -v
docker-compose up -d
```

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`
