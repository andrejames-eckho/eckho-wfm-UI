from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeRead


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=list[EmployeeRead])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@router.post("/", response_model=EmployeeRead, status_code=201)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(
        first_name=payload.first_name,
        last_name=payload.last_name,
        expected_start_time=payload.expected_start_time,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


