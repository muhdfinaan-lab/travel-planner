from typing import TypedDict
from langgraph.graph import StateGraph, END

from flight_agent import flight_agent
from accommodation_agent import accommodation_agent
from activity_agent import activity_agent


# 1. Define the shared state - every field an agent might read or write
class TripState(TypedDict):
    origin: str
    destination: str
    dates: str
    budget: str
    preferences: str
    flight_result: str
    accommodation_result: str
    activity_result: str
    final_itinerary: str


# 2. Define each node - a function that takes state, returns updates to it
def flight_node(state: TripState) -> dict:
    result = flight_agent(state["origin"], state["destination"], state["dates"], state["budget"])
    return {"flight_result": result}


def accommodation_node(state: TripState) -> dict:
    result = accommodation_agent(state["destination"], state["dates"], state["budget"])
    return {"accommodation_result": result}


def activity_node(state: TripState) -> dict:
    result = activity_agent(state["destination"], state["dates"], state["preferences"])
    return {"activity_result": result}


def combine_node(state: TripState) -> dict:
    combined = f"""# Your Trip to {state['destination']}

## ✈️ Flights
{state['flight_result']}

## 🏨 Accommodation
{state['accommodation_result']}

## 🗺️ Activities
{state['activity_result']}
"""
    return {"final_itinerary": combined}


# 3. Build the graph - wire the nodes together in order
graph = StateGraph(TripState)
graph.add_node("flight", flight_node)
graph.add_node("accommodation", accommodation_node)
graph.add_node("activity", activity_node)
graph.add_node("combine", combine_node)

graph.set_entry_point("flight")
graph.add_edge("flight", "accommodation")
graph.add_edge("accommodation", "activity")
graph.add_edge("activity", "combine")
graph.add_edge("combine", END)

app = graph.compile()


if __name__ == "__main__":
    result = app.invoke({
        "origin": "Kannur",
        "destination": "Tokyo",
        "dates": "Oct 10-17",
        "budget": "₹50,000",
        "preferences": "food, culture, some nightlife",
    })
    print(result["final_itinerary"])