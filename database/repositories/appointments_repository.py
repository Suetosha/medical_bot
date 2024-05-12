from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Appointments
from database.repositories.departments_repository import DepartmentsRepository
from database.repositories.doctors_repository import DoctorsRepository


class AppointmentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, patient, phone_number, department_id, doctor_id, datetime):
        self.session.add(Appointments(patient=patient, phone_number=phone_number, department_id=department_id,
                                      doctor_id=doctor_id, date_time=datetime))
        await self.session.commit()

    async def get_appointments(self):
        appointments = (await self.session.scalars(select(Appointments))).all()
        appointments = [f'{i.id}, {i.patient}' for i in appointments]
        return appointments

    async def get_appointment_by_id(self, id):
        app = (await self.session.execute(select(Appointments).filter_by(id=id))).scalar_one()

        depo_repo = DepartmentsRepository(self.session)
        doc_repo = DoctorsRepository(self.session)

        department = await depo_repo.get_department_by_id(app.department_id)
        doctor = await doc_repo.get_doctor_by_id(app.doctor_id)

        date = datetime.strftime(app.date_time, '%d/%m/%Y')
        time = datetime.strftime(app.date_time, '%H:%M')

        app = {'patient': app.patient, 'department': department,
               'doctor': doctor, 'doctor_id': app.doctor_id, 'date': date, 'time': time}

        return app

    async def delete_appointment(self, app_id):
        await self.session.execute(delete(Appointments).where(Appointments.id == app_id))
        await self.session.commit()

    async def update_appointment(self, data) -> None:

        await self.session.execute(update(Appointments).where(Appointments.id == data['id']).values(
            patient=data['name'],
            phone_number=data['phone_number'],
            department_id=data['department_id'],
            doctor_id=data['doctor_id'],
            date_time=data['date']
        ))
        await self.session.commit()
