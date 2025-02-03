from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Crew
from agents import TravelAgents
from tasks import TravelTasks
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class TripRequest(BaseModel):
    origin_city: str
    cities: str
    travel_dates: str
    interests: str
    budget: float

@app.post("/plan-trip/")
def plan_trip(request: TripRequest):
    agents = TravelAgents()
    tasks = TravelTasks()

    expert_agent = agents.expert_travel_agent()
    city_expert = agents.city_selection_expert()
    tour_guide = agents.local_tour_guide()
    budget_planner = agents.budget_planner()

    task1 = tasks.plan_itinerary(expert_agent, request.origin_city, request.cities, request.travel_dates, request.interests, request.budget)
    task2 = tasks.select_cities(city_expert, request.origin_city, request.cities, request.travel_dates, request.interests, request.budget)
    task3 = tasks.find_local_tour_guide(tour_guide, request.cities, request.travel_dates, request.interests, request.budget)
    task4 = tasks.create_budget(budget_planner, request.cities, request.travel_dates, request.interests, "all", request.budget)

    crew = Crew(agents=[expert_agent, city_expert, tour_guide, budget_planner], tasks=[task1, task2, task3, task4], verbose=True)

    result = crew.kickoff()
    
    return {"trip_plan": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
