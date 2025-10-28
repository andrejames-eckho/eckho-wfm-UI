# Eckho WFM Backend API

A FastAPI-based backend for Eckho Workforce Management system, handling user management and time tracking.

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd eckho-wfm-UI/backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Database Setup
```bash
# Create database and run migrations
python -c "from app.database import engine; from app import models; models.Base.metadata.create_all(bind=engine)"
```

### 6. Run the Application
```bash
uvicorn app.main:app --reload
```

## 📚 API Documentation

Once running, access the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

All endpoints (except public ones) require authentication. Include the JWT token in the `Authorization` header:
```
Authorization: Bearer <your_jwt_token>
```

## 📡 API Endpoints

### 👥 Users

#### Create User
**`POST /users/`**
```json
{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "department": "Field"
}
```
**Response (201 Created)**
```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "department": "Field",
  "created_at": "2025-10-28T12:00:00Z"
}
```

#### List Users
**`GET /users/`**
**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `department` (str, optional): Filter by department
- `active_only` (bool, optional): Only return active users (default: true)

**Response (200 OK)**
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "department": "Field",
    "created_at": "2025-10-28T12:00:00Z"
  }
]
```

#### Get User Details
**`GET /users/{user_id}`**
**Response (200 OK)**
```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "department": "Field",
  "created_at": "2025-10-28T12:00:00Z",
  "time_records": [
    {
      "id": 1,
      "user_id": 1,
      "date": "2025-10-28",
      "time": "09:00:00",
      "record_type": "Time In",
      "created_at": "2025-10-28T09:00:00Z"
    }
  ]
}
```

#### Update User
**`PUT /users/{user_id}`**
```json
{
  "first_name": "Johnathan",
  "department": "Warehouse"
}
```
**Response (200 OK)**
```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "Johnathan",
  "last_name": "Doe",
  "department": "Warehouse",
  "created_at": "2025-10-28T12:00:00Z"
}
```

#### Delete User
**`DELETE /users/{user_id}`**
**Response (200 OK)**
```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "Johnathan",
  "last_name": "Doe",
  "department": "Warehouse",
  "created_at": "2025-10-28T12:00:00Z"
}
```

### ⏱️ Time Records

#### Create Time Record
**`POST /time-records/`**
```json
{
  "user_id": 1,
  "date": "2025-10-28",
  "time": "09:00:00",
  "record_type": "Time In"
}
```
**Response (201 Created)**
```json
{
  "id": 1,
  "user_id": 1,
  "date": "2025-10-28",
  "time": "09:00:00",
  "record_type": "Time In",
  "created_at": "2025-10-28T09:00:00Z"
}
```

#### List Time Records
**`GET /time-records/`**
**Query Parameters:**
- `user_id` (int, optional): Filter by user ID
- `start_date` (date, optional): Filter by start date (YYYY-MM-DD)
- `end_date` (date, optional): Filter by end date (YYYY-MM-DD)
- `record_type` (string, optional): Filter by record type (TIME_IN, TIME_OUT, BREAK_IN, BREAK_OUT)
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)

**Response (200 OK)**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "date": "2025-10-28",
    "time": "09:00:00",
    "record_type": "Time In",
    "created_at": "2025-10-28T09:00:00Z"
  }
]
```

#### Get Time Record
**`GET /time-records/{record_id}`**
**Response (200 OK)**
```json
{
  "id": 1,
  "user_id": 1,
  "date": "2025-10-28",
  "time": "09:00:00",
  "record_type": "Time In",
  "created_at": "2025-10-28T09:00:00Z"
}
```

#### Get User's Time Records
**`GET /time-records/user/{user_id}`**
**Query Parameters:** Same as list time records
**Response (200 OK)**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "date": "2025-10-28",
    "time": "09:00:00",
    "record_type": "Time In",
    "created_at": "2025-10-28T09:00:00Z"
  }
]
```

#### Get Daily Summary
**`GET /time-records/user/{user_id}/daily-summary/{date}`**
**Response (200 OK)**
```json
{
  "date": "2025-10-28",
  "user_id": 1,
  "time_in": "09:00:00",
  "time_out": "17:00:00",
  "breaks": [
    {"start": "12:00:00", "end": "12:30:00", "duration_minutes": 30}
  ],
  "total_break_time_minutes": 30,
  "total_work_time_minutes": 450
}
```

#### Delete Time Record
**`DELETE /time-records/{record_id}`**
**Response (200 OK)**
```json
{
  "id": 1,
  "user_id": 1,
  "date": "2025-10-28",
  "time": "09:00:00",
  "record_type": "Time In",
  "created_at": "2025-10-28T09:00:00Z"
}
```

#### Filtering Time Records
- `GET /time-records/?user_id=1` - Filter by user
- `GET /time-records/?start_date=2025-01-01&end_date=2025-12-31` - Date range
- `GET /time-records/?record_type=TIME_IN` - Filter by record type
- `GET /time-records/?skip=0&limit=50` - Pagination

## 🔄 Record Types

| Type | Description |
|------|-------------|
| `TIME_IN` | Employee starts their workday |
| `TIME_OUT` | Employee ends their workday |
| `BREAK_IN` | Employee starts a break |
| `BREAK_OUT` | Employee ends a break |

## 🏗️ Department Types

| Type | Description |
|------|-------------|
| `Field` | Field operations employees |
| `Warehouse` | Warehouse employees |

## 📦 Services

The backend is organized into service layers:

### User Service (`user_service.py`)
- User CRUD operations
- User activation/deactivation
- Department-based user queries

### Time Record Service (`time_record_service.py`)
- Time record CRUD operations
- Time calculations and validations
- Daily summaries and reporting

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/eckho_wfm

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# Application
DEBUG=true
ENVIRONMENT=development
```

## 🛠 Development

### Code Style
```bash
# Format code
black .

# Lint code
flake8

# Run tests
pytest
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## 📄 License

[Your License Here]

## 📞 Support

For support, please contact [Your Support Email]
