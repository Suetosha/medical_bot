import datetime

from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String, ForeignKey, Time, Date


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=False)


class Faq(Base):
    __tablename__ = 'faq'

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)


class CallRequest(Base):
    __tablename__ = 'call_request'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    problem: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)


class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)


class Department(Base):
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)


class Doctor(Base):
    __tablename__ = 'doctors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped[Department] = relationship()


class Slot(Base):
    __tablename__ = 'slots'

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[datetime.time] = mapped_column(Time)

    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    doctor: Mapped[Doctor] = relationship()


class Appointment(Base):
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(primary_key=True)
    patient: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    date: Mapped[datetime.date] = mapped_column(Date)
    time: Mapped[datetime.time] = mapped_column(Time)

    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    doctor: Mapped[Doctor] = relationship()
