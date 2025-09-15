from sqlalchemy import Column, Date, Integer, String, Time, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    expected_start_time = Column(String(20), nullable=True)

    credentials = relationship("UserCredential", back_populates="employee", uselist=False)
    time_records = relationship("TimeRecord", back_populates="employee", cascade="all, delete-orphan")


class UserCredential(Base):
    __tablename__ = "user_credentials"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    employee = relationship("Employee", back_populates="credentials")


class TimeRecord(Base):
    __tablename__ = "time_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    expected_time_in = Column(String(20), nullable=True)
    expected_time_out = Column(String(20), nullable=True)
    time_in = Column(String(20), nullable=True)
    time_out = Column(String(20), nullable=True)
    break_in = Column(String(20), nullable=True)
    break_out = Column(String(20), nullable=True)
    status = Column(String(50), nullable=True)

    employee = relationship("Employee", back_populates="time_records")


