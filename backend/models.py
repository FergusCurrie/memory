from datetime import date
from sqlalchemy import ForeignKey

# Declarative mapping = write python objects, sql alchemy creates sql objects
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

# class Dataset(Base):
#     __tablename__ = "code"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     description: Mapped[str]
#     date_created: Mapped[date] = mapped_column(default=func.current_date())


class Base(DeclarativeBase):
    pass


class Problem(Base):
    __tablename__ = "problem"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    date_created: Mapped[date] = mapped_column(default=func.current_date())


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    date_created: Mapped[date] = mapped_column(default=func.current_date())
    problem_id: Mapped["Problem"] = mapped_column(ForeignKey("problem.id"))


class Code(Base):
    __tablename__ = "code"

    id: Mapped[int] = mapped_column(primary_key=True)
    code_table_name: Mapped[str]
    # preprocessing_code: Mapped[str]
    date_created: Mapped[date] = mapped_column(default=func.current_date())
    problem_id: Mapped["Problem"] = mapped_column(ForeignKey("problem.id"))


class Dataset(Base):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    date_created: Mapped[date] = mapped_column(default=func.current_date())


from sqlalchemy import create_engine

conn_url = "postgresql+psycopg2://ferg234e1341:32rsrg5ty3t%gst42@postgres_db/memory_db"

engine = create_engine(conn_url)

# with Session(engine) as session:

Problem.metadata.create_all(engine)
Review.metadata.create_all(engine)
Dataset.metadata.create_all(engine)
Code.metadata.create_all(engine)
