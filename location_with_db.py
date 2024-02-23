from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select
from models.location_model import create_location, Location , update_location ,create_db_and_tables
from database.database_model import engine

app = FastAPI(
    title="FastAPI with Database",
    description="In this Api we use neon database and connect it with fast api",
    version="1.0.0",
    servers = [
    {
      "url": "https://dashing-kit-pet.ngrok-free.app/",
      "description": "Production Server",
    },
    {
        "url": "http://127.0.0.1:8000",
        "description": "Local Server",
    }
  ],
)

@app.on_event("startup")
def on_startup():
    """
    Handle the "startup" event by creating the necessary database and tables.
    """
    create_db_and_tables()

@app.get("/persons/")
def read_all_persons():
    """
    Retrieves all persons from the database.

    Returns:
        A list of dictionaries containing the data of all persons.
    """
    with Session(engine) as session:
        persons_data = session.exec(select(Location)).all()
        return persons_data
    
@app.post("/create_person")
def create_person(person_data: create_location):
    """
    create_person function creates a new person record in the database using the provided person_data.

    Parameters:
    - person_data: Location - the data for the new person record.

    Returns:
    - Location: the newly created person record.
    """
    person = Location.model_validate(person_data)
    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)
        return {"message": "Person created successfully", "person_data": person}
    
@app.get("/get_person/{name}")
def read_person(name: str):
    """
    A function that reads person data based on the provided name parameter and returns the person data. 

    Parameters:
    - name: a string representing the name of the person to retrieve

    Returns:
    - person_data: the data of the person identified by the provided name
    """
    with Session(engine) as session:
        person_data = session.exec(select(Location).where(Location.name == name)).first()
        if not person_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
        return person_data


@app.put("/update_person/{person_name}")
def update_data(person_name:str , person_data: update_location):
    with Session(engine) as session:
        person = session.exec(select(Location).where(Location.name == person_name)).first()
        if not person:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
        data = person_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(person, key, value)
        session.add(person)
        session.commit()
        session.refresh(person)
        return person

@app.delete("/delete_person/{name}")
def delete_person(name:str):
    """
    Deletes a person with the specified name from the database.

    Parameters:
    - name: str, the name of the person to be deleted

    Returns:
    - dict, a message indicating the success of the deletion
    """
    with Session(engine) as session:
        person = session.exec(select(Location).where(Location.name == name)).first()
        if not person:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
        session.delete(person)
        session.commit()
        return {"message": "Person deleted successfully"}
