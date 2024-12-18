from sqlalchemy import Table, Column, Integer, String, Float, MetaData, Text

metadata = MetaData()

deposits = Table(
    "deposits",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", String, nullable=False),
    Column("periods", Integer, nullable=False),
    Column("amount", Float, nullable=False),
    Column("rate", Float, nullable=False),
    Column("result", Text, nullable=False)
)
