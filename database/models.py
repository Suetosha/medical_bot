from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Boolean


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=False)




