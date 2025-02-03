# To know more about the Task class, visit: https://docs.crewai.com/concepts/tasks
try:
    from crewai import Task
except ImportError:
    raise ImportError(
        "CrewAI is not installed. Please install it using: "
        "pip install crewai"
    )
from textwrap import dedent

#This is an example of how to define custom tasks 
# you can define as many tasks as you want.
# You can also define custom agents in agents.py

class TravelTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def plan_itinerary(self, agent, origin_city, cities, travel_dates, interests, budget):
        return Task(
            description=f"""
            **Task**: Create a detailed travel itinerary based on the following information:
            - Origin City: {origin_city}
            - Destination Cities: {cities}
            - Travel Dates: {travel_dates}
            - Interests: {interests}
            - Budget: ${budget}

            Please provide a comprehensive day-by-day itinerary that maximizes the travel experience while staying within budget.
            Consider transportation between cities, accommodation, and activities that match the interests.
            """,
            agent=agent,
            expected_output="""Provide a detailed day-by-day itinerary in the following format:
            Day 1:
            - Morning: [Activities]
            - Afternoon: [Activities]
            - Evening: [Activities]
            - Accommodation: [Hotel/Place]
            
            Include estimated costs for each day and ensure the total stays within budget."""
        )

    def select_cities(self, agent, origin_city, cities, travel_dates, interests, budget):
        # Convert comma-separated string to list if needed
        city_list = [c.strip() for c in cities.split(',')] if isinstance(cities, str) else cities
        return Task(
            description=dedent(
                f'''
                **Task**: Identify the best cities to visit based on the provided list.
                **Description**: Analyze the suggested cities ({', '.join(city_list)}) and recommend the best ones to visit based on traveler preferences and interests. Consider factors such as weather patterns, seasonal events, attractions, accessibility, budget, and travel time from {origin_city}.
                **Parameters**:
                - Origin City: {origin_city}
                - Cities: {cities}
                - Travel Dates: {travel_dates}
                - Interests: {interests}
                - Budget: ${budget}
                **Expected Output**: A list of recommended cities with brief justifications for each selection.
                {self.__tip_section()}
                '''
            ),
            agent=agent,
            expected_output="Provide a prioritized list of cities with brief justification for each selection based on interests and budget."
        )

    def find_local_tour_guide(self, agent, cities, travel_dates, interests, budget):
        return Task(
            description=dedent(
                f'''
                **Task**: Find a reliable local tour guide for {cities}.
                **Description**: Research and recommend a qualified local tour guide with positive reviews and reasonable pricing.
                **Parameters**:
                - Cities: {cities}
                - Travel Dates: {travel_dates}
                - Interests: {interests}
                - Budget: ${budget}
                **Expected Output**: Contact details, pricing, and availability of at least three local tour guides.
                {self.__tip_section()}
                '''
            ),
            agent=agent,
            expected_output="Provide specific local recommendations and insider tips for each city, including best times to visit specific attractions and local customs to be aware of."
        )

    def create_budget(self, agent, cities, travel_dates, interests, transport_mode, budget):
        return Task(
            description=dedent(
                f'''
                **Task**: Develop a detailed budget plan for the trip 
                **Description**: Break down costs for flights, accommodation, daily activities, meals, and transportation ({transport_mode}). Identify cost-saving strategies without compromising experience.
                **Parameters**:
                - Cities: {cities}
                - Travel Dates: {travel_dates}
                - Interests: {interests}
                - Budget: ${budget}
                **Expected Output**: A cost breakdown with a total estimated budget and recommendations for savings.
                {self.__tip_section()}
                '''
            ),
            agent=agent,
            expected_output="Provide a detailed budget breakdown by category (accommodation, transportation, activities, food) for each city, with specific cost estimates and recommendations for saving money."
        )
