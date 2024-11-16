Relationships:

- related = relationship("RelatedClass")

```
related = relationship("RelatedClass")

related_items: Mapped[List["RelatedItem"]] = relationship()
# many-to-one or one-to-one relationship:
related_item: Mapped["RelatedItem"] = relationship()
parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
```

Relationship vs foreign key:

- Relationship is at python object level, vis to app. Foreign key for db

Many-Many:
Fix manual sql is briding/joining table.
In SA, use Associatino object: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object

Example without SA special constructs:

```
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Association(Base):
    __tablename__ = "association_table"
    left_id: Mapped[int] = mapped_column(ForeignKey("left_table.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(
        ForeignKey("right_table.id"), primary_key=True
    )
    extra_data: Mapped[Optional[str]]
    child: Mapped["Child"] = relationship()


class Parent(Base):
    __tablename__ = "left_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Association"]] = relationship()


class Child(Base):
    __tablename__ = "right_table"
    id: Mapped[int] = mapped_column(primary_key=True)
```

Can replace with:

```

class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # many-to-many relationship to Child, bypassing the `Association` class
    children: Mapped[List["Child"]] = relationship(
        secondary="association_table", back_populates="parents"
    )

    # association between Parent -> Association -> Child
    child_associations: Mapped[List["Association"]] = relationship(
        back_populates="parent"
    )


class Child(Base):
    __tablename__ = "right_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # many-to-many relationship to Parent, bypassing the `Association` class
    parents: Mapped[List["Parent"]] = relationship(
        secondary="association_table", back_populates="children"
    )

    # association between Child -> Association -> Parent
    parent_associations: Mapped[List["Association"]] = relationship(
        back_populates="child"
    )
```
