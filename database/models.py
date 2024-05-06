from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String


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


class Services(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    service: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)


