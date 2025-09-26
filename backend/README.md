# Time Tracking API

A FastAPI-based backend for managing users and their time records.

## Setup

1. **Prerequisites**
   - Python 3.8+
   - PostgreSQL
   - pip (Python package manager)

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   - Create a PostgreSQL database named `time_tracking_db`
   - Copy `.env.example` to `.env` and update the database credentials

4. **Run migrations**
   ```bash
   # From the backend directory
   python -c "from app.database import engine; from app import models; models.Base.metadata.create_all(bind=engine)"
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, you can access:
- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user details with time records

### Time Records
- `POST /time-records/` - Create a new time record
- `GET /time-records/` - List all time records
- `GET /users/{user_id}/time-records/` - Get time records for a specific user

## Environment Variables

See `.env.example` for required environment variables. Copy to `.env` and update the values.

## Development

- **Code Formatting**: `black .`
- **Linting**: `flake8`
- **Testing**: `pytest` (coming soon)
