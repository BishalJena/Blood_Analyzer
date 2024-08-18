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
    
    medical_analyst = Agent(
        role='Medical Analyst',
        goal='Analyze the blood test report and provide a summary in simple terms.',
        backstory="An expert in interpreting medical data and explaining it to non-medical people.",
        verbose=True,
        allow_delegation=False
    )

    health_researcher = Agent(
        role='Health Researcher',
        goal='Search the internet for articles based on the blood test analysis. You should then search the web for articles tailored to the person\'s health needs based on the blood test results',
        backstory="Skilled at finding accurate and relevant health information online.",
        verbose=True,
        allow_delegation=False,
        tools=[SerperDevTool(api_key=env_vars["SERPER_API_KEY"])]
    )

    health_advisor = Agent(
        role='Health Advisor',
        goal='Provide health recommendations based on the articles and blood test summary.',
        backstory="Experienced in providing personalized health advice.",
        verbose=True,
        allow_delegation=False
    )

    return medical_analyst, health_researcher, health_advisor