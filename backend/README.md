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

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Create a new user |
| `GET` | `/users/` | List all users (with pagination) |
| `GET` | `/users/{user_id}` | Get user details with time records |
| `PUT` | `/users/{user_id}` | Update user information |
| `DELETE` | `/users/{user_id}` | Delete a user |
| `POST` | `/users/{user_id}/deactivate` | Deactivate a user |
| `POST` | `/users/{user_id}/activate` | Activate a user |

#### Filtering Users
- `GET /users/?department=Engineering` - Filter by department
- `GET /users/?active_only=true` - Only show active users
- `GET /users/?skip=10&limit=20` - Pagination

### ⏱️ Time Records

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/time-records/` | Create a new time record |
| `GET` | `/time-records/` | List all time records (with filters) |
| `GET` | `/time-records/{record_id}` | Get specific time record |
| `GET` | `/time-records/user/{user_id}` | Get user's time records |
| `GET` | `/time-records/user/{user_id}/daily-summary/{date}` | Get daily summary |
| `DELETE` | `/time-records/{record_id}` | Delete a time record |

#### Filtering Time Records
- `GET /time-records/?user_id=1` - Filter by user
- `GET /time-records/?start_date=2025-01-01&end_date=2025-12-31` - Date range
- `GET /time-records/?record_type=TIME_IN` - Filter by record type
- `GET /time-records/?skip=0&limit=50` - Pagination

## 🔄 Record Types

- `TIME_IN` - Employee starts their workday
- `TIME_OUT` - Employee ends their workday
- `BREAK_IN` - Employee starts a break
- `BREAK_OUT` - Employee ends a break

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
