import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "tools")))

from tools import CalculatorTools, SearchTools

from crewai import Agent
from textwrap import dedent
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    try:
        from langchain.chat_models import ChatOpenAI
    except ImportError:
        raise ImportError(
            "Required packages are not installed. Please install with: "
            "pip install langchain-openai python-dotenv openai"
        )
try:
    from tools import CalculatorTools, SearchTools

except ImportError:
    try:
       from tools import CalculatorTools, SearchTools
    except ImportError:
        raise ImportError(
            "Could not import tools. Please ensure:\n"
            "1. Your tools directory is in the correct location\n"
            "2. You're running the code from the project root directory\n"
            "3. The tools directory has an __init__.py file\n"
            "4. The module names match exactly (case-sensitive)"
        )

class TravelAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        self.search_tools = SearchTools()
        self.calculator_tools = CalculatorTools()

    def get_search_tool(self):
        return self.search_tools.search_internet

    def get_calculator_tool(self):
        return self.calculator_tools.calculate

    def expert_travel_agent(self):
        return Agent(
            role="Expert Travel Agent",
            backstory=dedent(f"""I am a seasoned travel agent with 15 years of experience planning 
            international trips. I've helped thousands of clients create memorable vacations while 
            staying within their budget. I have extensive knowledge of global destinations, travel 
            regulations, and industry best practices."""),
            goal=dedent(f"""Create a comprehensive 7-day travel itinerary that maximizes the client's 
            experience while adhering to their budget and preferences. Coordinate with other experts 
            to ensure all aspects of the trip are properly planned."""),
            tools=[self.get_search_tool(), self.get_calculator_tool()],
            allow_delegation=True,
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def city_selection_expert(self):
        return Agent(
            role="City Selection Expert",
            backstory=dedent(f"""I am an expert in global destinations with deep knowledge of 
            cities worldwide. I analyze travel trends, seasonal patterns, and local events to 
            recommend the best destinations for each traveler's interests and timing."""),
            goal=dedent(f"""Research and recommend the most suitable cities based on the 
            traveler's preferences, considering factors like weather, local events, and 
            accessibility."""),
            tools=[self.get_search_tool()],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            backstory=dedent(f"""I am a professional tour guide with expertise in creating 
            engaging local experiences. I know the hidden gems, best local restaurants, and 
            cultural hotspots that make each destination special."""),
            goal=dedent(f"""Design daily itineraries that showcase the best experiences at 
            each destination, including cultural activities, local cuisine, and notable 
            attractions."""),
            tools=[self.get_search_tool()],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def budget_planner(self):
        return Agent(
            role="Budget Planner",
            backstory=dedent(f"""I am a financial expert specializing in travel budgeting. 
            I have helped hundreds of travelers maximize their experiences while maintaining 
            strict budget controls."""),
            goal=dedent(f"""Create detailed cost breakdowns for all aspects of the trip 
            and identify opportunities for savings without compromising the travel 
            experience."""),
            tools=[self.get_calculator_tool(), self.get_search_tool()],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )
