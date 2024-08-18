from crewai import Agent
from crewai_tools import SerperDevTool
from utils import load_environment_variables

def initialize_agents():
    """
    Initializes and returns the agents used in the application.

    Returns:
        tuple: A tuple containing the initialized agents.
    """
    env_vars = load_environment_variables()
    
    researcher = Agent(
        role='Researcher',
        goal='Analyze the blood test report and give the data with values of all blood parameters in string.',
        backstory='You are an AI medical assistant specializing in analyzing blood test reports and presenting the data with detailed levels/data of each parameter.',
        verbose=True,
        allow_delegation=False
    )

    health_advisor = Agent(
        role='Health Advisor',
        goal='Provide health recommendations based on the blood test report summary.',
        backstory='You are an AI health advisor specializing in giving personalized health recommendations based on detailed analysis of blood reports.',
        verbose=True,
        allow_delegation=False
    )

    webmd_finder = Agent(
        role='WebMD Finder',
        goal='Find four relevant WebMD articles based on the health recommendations provided.',
        backstory='You are an AI assistant specializing in finding accurate and relevant WebMD articles based on health advice provided.',
        verbose=True,
        allow_delegation=False,
        tools=[SerperDevTool(api_key=env_vars["SERPER_API_KEY"])]
    )

    return researcher, health_advisor, webmd_finder