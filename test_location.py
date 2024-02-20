from fastapi.testclient import TestClient
from location import app, Location, get_location_or_404
from fastapi import HTTPException

location = {
    "ubaid" : Location(name="Ubaid", location="Karachi"),
    "ali" : Location(name="Ali", location="Lahore"),
}

def get_fake_loc_or_404(name:str)->Location:
    loc = location.get(name.lower())
    print(loc)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    return loc

app.dependency_overrides[get_location_or_404] = get_fake_loc_or_404
client = TestClient(app)
def test_read_Location():
    response = client.get("/locations/ubaid")
    assert response.status_code == 200
    assert response.json() == {"name": "Ubaid", "location": "Karachi"}

def test_read_Location_not_found():
    response = client.get("/locations/unknown")
    assert response.status_code == 404