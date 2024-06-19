from sqlalchemy import Table, Column, String, Integer, MetaData
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass
     
class ValuesOrm(Base):
    __tablename__ = "values"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    value: Mapped[str]


















# metadata_obj = MetaData()

# values_table = Table(
#     "values",
#     metadata_obj,
#     Column("id",Integer ,primary_key=True),
#     Column("user_id", String),
#     Column("value", String)
# )