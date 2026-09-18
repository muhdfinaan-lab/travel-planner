from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from orchestrator import app as orchestrator_app

app = FastAPI(title="Travel Planner API")

# Allow the frontend (served separately or from the same origin) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    origin: str
    destination: str
    dates: str
    budget: str
    preferences: str


@app.post("/plan-trip")
def plan_trip(request: TripRequest):
    result = orchestrator_app.invoke({
        "origin": request.origin,
        "destination": request.destination,
        "dates": request.dates,
        "budget": request.budget,
        "preferences": request.preferences,
    })
    return {"itinerary": result["final_itinerary"]}


# Serve the frontend files (we'll create this folder in Step 5b)
app.mount("/", StaticFiles(directory="static", html=True), name="static")