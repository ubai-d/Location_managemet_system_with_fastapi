from sqlmodel import Field, SQLModel
from typing import Optional
from database.database_model import engine
class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location: str
class update_location(SQLModel):
    id : int 
    name : str 
    location : str


def create_db_and_tables():
    """
    Create the database and tables using the SQLModel metadata and engine.
    """
    SQLModel.metadata.create_all(engine)
