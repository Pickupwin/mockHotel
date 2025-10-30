from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class InvokeRequest(BaseModel):
    location: str


class Hotel(BaseModel):
    name: str
    price: float
    rating: float


app = FastAPI(title="Mock Hotel API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/invoke")
def invoke(req: InvokeRequest) -> list[Hotel]:
    # Static demo data regardless of location
    hotels: list[Hotel] = [
        Hotel(name="Sunrise Hotel", price=129.0, rating=4.5),
        Hotel(name="City Center Inn", price=89.0, rating=4.1),
        Hotel(name="Lakeside Resort", price=159.0, rating=4.7),
        Hotel(name="Budget Stay", price=59.0, rating=3.9),
        Hotel(name="Grand Palace", price=199.0, rating=4.8),
    ]
    return hotels


# To run locally:
#   uvicorn backend.mock_api.main:app --reload --host 0.0.0.0 --port 8000


