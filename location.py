from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
class Location(BaseModel):
    name :  str
    location : str

Locations = {
    "ubaid" : Location(name="Ubaid", location="Karachi"),
    "ali" : Location(name="Ali", location="Lahore"),
    "hamza" : Location(name="Hamza", location="Islamabad"),
}

def get_location_or_404(name : str)->Location:
    """
    Get the location by name or raise a 404 error if not found.

    Parameters:
    name (str): the name of the location to retrieve.

    Returns:
    Location: the location object if found.
    """
    loc = Locations.get(name.lower())
    if not loc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return loc

@app.get("/locations/{name}")
def get_location(name : str,location:Annotated[Location,Depends(get_location_or_404)])->Location :
    """
    Retrieve a location by name.

    Parameters:
        name (str): The name of the location.
        location (Annotated[Location, Depends(get_location_or_404)]): The annotated location.

    Returns:
        Location: The retrieved location.
    """
    return location
