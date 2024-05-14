from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Slot, Doctor
from sqlalchemy import select, delete


class SlotsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, doctor_id, doctor, time):
        if time in await self.get_doctor_slots(doctor):
            return False
        self.session.add(Slot(doctor_id=doctor_id, time=time))
        await self.session.commit()
        return True

    async def get_doctor_slots(self, doctor_name):
        slots = (await self.session.execute(select(Slot.time)
                                            .join(Doctor)
                                            .filter_by(name=doctor_name).order_by(Slot.time))).scalars()
        slots = [i for i in slots]
        return slots

    async def delete(self, doctor_name, time):
        slot = (await self.session.scalars(select(Slot).join(Doctor)
                                           .filter(Doctor.name == doctor_name, Slot.time == time))).first()
        await self.session.delete(slot)
        await self.session.commit()


