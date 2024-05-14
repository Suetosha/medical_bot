from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Appointment, Doctor, Department


class AppointmentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, patient, phone_number, doctor_id, date, time):
        self.session.add(Appointment(patient=patient, phone_number=phone_number,
                                     doctor_id=doctor_id, date=date, time=time))
        await self.session.commit()

    async def get_all(self):
        appointments = (await self.session.scalars(select(Appointment))).all()
        appointments = [f'{i.id}, {i.patient}' for i in appointments]
        return appointments

    async def get_by_date_and_doctor_name(self, selected_date, doctor_name):
        closed_slots = (await self.session.execute(select(Appointment.time)
                                                   .join(Doctor)
                                                   .filter_by(name=doctor_name)
                                                   .filter(Appointment.date == selected_date)
                                                   .order_by(Appointment.time))).scalars()
        return closed_slots

    async def get_by_id(self, app_id):
        res = (await self.session.execute(select(Appointment, Doctor, Department)
                                          .join(Appointment.doctor)
                                          .join(Doctor.department)
                                          .filter(Appointment.id == app_id))).first()

        if res is not None:
            app = res[0]
            app = {'patient': app.patient, 'department': app.doctor.department.name,
                   'department_id': app.doctor.department_id, 'doctor_id': app.doctor.id,
                   'doctor': app.doctor.name, 'date': app.date, 'time': app.time}

            return app

    async def delete(self, app_id):
        await self.session.execute(delete(Appointment).where(Appointment.id == app_id))
        await self.session.commit()

    async def update(self, data) -> None:

        await self.session.execute(update(Appointment).where(Appointment.id == data['id']).values(
            patient=data['name'],
            phone_number=data['phone_number'],
            doctor_id=data['doctor_id'],
            date=data['date'],
            time=data['time']
        ))
        await self.session.commit()
