from datetime import date
from sqlalchemy import ForeignKey, String

# Declarative mapping = write python objects, sql alchemy creates sql objects
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List, Optional


class Base(DeclarativeBase):
    pass


class Problem(Base):
    __tablename__ = "problem"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    date_created: Mapped[date] = mapped_column(default=func.current_date())


class Review(Base):
    __tablename__ = "code"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    date_created: Mapped[date] = mapped_column(default=func.current_date())


class Datasets(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    date_created: Mapped[date] = mapped_column(default=func.current_date())
    problem_id: Mapped["Problem"] = relationship(back_populates="user", cascade="all, delete-orphan")


class Code(Base):
    __tablename__ = "code"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    preprocessing_code: Mapped[str]
    date_created: Mapped[date] = mapped_column(default=func.current_date())
    problem_id: Mapped["Problem"] = relationship(back_populates="user", cascade="all, delete-orphan")


###################
class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


from sqlalchemy import create_engine

conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

engine = create_engine(conn_url)

# with Session(engine) as session:
from sqlalchemy import String

Address.metadata.create_all(engine)
User.metadata.create_all(engine)
Dataset.metadata.create_all(engine)
