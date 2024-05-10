from datetime import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Appointments, Slots
from sqlalchemy import select, delete


class SlotsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_slots(self, doctor_id, time):
        if time in await self.get_doctor_slots(doctor_id):
            return True
        self.session.add(Slots(doctor_id=doctor_id, time=time))
        await self.session.commit()
        return False

    async def get_doctor_slots(self, doctor_id):
        slots = (await self.session.execute(select(Slots).filter_by(doctor_id=doctor_id))).scalars()
        slots = list(sorted([i.time for i in slots]))
        return slots

    async def get_opened_slots(self, day,  doctor_id):
        all_slots = await self.get_doctor_slots(doctor_id)
        closed_slots = (await self.session.execute(select(Appointments).filter_by(doctor_id=doctor_id))).scalars()

        closed_slots = [i.date_time for i in closed_slots]

        closed_slots = [dt.strftime(i, '%H:%M') for i in closed_slots if i.date().day == day]

        free_slots = list(sorted([i for i in all_slots if i not in closed_slots]))

        return free_slots

    async def delete_slot(self, doctor_id, time):
        await self.session.execute(delete(Slots).where(Slots.doctor_id == doctor_id, Slots.time == time))
        await self.session.commit()


