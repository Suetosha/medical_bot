from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Appointments


class AppointmentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, patient, department_id, doctor_id, datetime):
        self.session.add(Appointments(patient=patient, department_id=department_id,
                                      doctor_id=doctor_id, date_time=datetime))
        await self.session.commit()

    async def get_appointments(self):
        appointments = (await self.session.scalars(select(Appointments))).all()
        appointments = [f'{i.id}, {i.patient}' for i in appointments]
        return appointments

    async def get_appointment_by_id(self, id):
        app = (await self.session.execute(select(Appointments).filter_by(id=id))).scalar_one()
        return app

    async def update_appointment(self, data) -> None:

        await self.session.execute(update(Appointments).where(Appointments.id == data['id']).values(
            patient=data['name'],
            department_id=data['department_id'],
            doctor_id=data['doctor_id'],
            date_time=data['date']
        ))
        await self.session.commit()
