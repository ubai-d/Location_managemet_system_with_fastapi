from sqlmodel import Field, SQLModel
from typing import Optional
from database.database_model import engine
class Location_base(SQLModel):
    name: str = Field(index=True)
    location: str

class Location(Location_base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
class create_location(Location_base):
    pass
class update_location(SQLModel):
    name : str 
    location : str

def create_db_and_tables():
    """
    Create the database and tables using the SQLModel metadata and engine.
    """
    SQLModel.metadata.create_all(engine)
