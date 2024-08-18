from crewai import Task
from crewai_tools import SerperDevTool
from utils import load_environment_variables

def initialize_tasks(medical_analyst, health_researcher, health_advisor, blood_test_text):
    """
    Initializes and returns the tasks used in the application.

    Args:
        medical_analyst (Agent): The medical analyst agent.
        health_researcher (Agent): The health researcher agent.
        health_advisor (Agent): The health advisor agent.
        blood_test_text (str): The extracted text from the blood test report.

    Returns:
        list: A list of initialized tasks.
    """
    env_vars = load_environment_variables()

    analyze_blood_test = Task(
        description=f'Details of patient on the top then analyze the following blood test report and provide a summary: {blood_test_text}',
        agent=medical_analyst,
        expected_output='Details of patient on the top, summary of the blood test in simple terms.'
    )

    search_for_articles = Task(
        description='Search the web for articles relevant to the health issues identified in the blood test summary.',
        agent=health_researcher,
        expected_output='A list of articles with URLs and a brief description of each.'
    )

    provide_recommendations = Task(
        description='''
        Provide health recommendations based on the articles and blood test summary. Give health recommendations and provide links to the relevant articles.
        ''',
        expected_output='''
        A complete summary of the full report in simple easy-to-understand terms 
        followed by all levels from the entire report in table format followed by a bullet list of actionable health recommendations, with each bullet point containing 
        links to its source // FOLLOW GIVEN FORMAT !!! //

        ## Summary
        [Provide a simple short summary of the blood report here with blood parameter levels like haemoglobin, wbc count etc, **If needed only do this step:-(Example:-Use data from blood report like (total platlets level[use from the orignal blood report ]))**]

        ## Levels
        | Parameter | Level | Normal Range |

        ## Recommendations
        - [Recommendation 1 (ex:- eat healthy)](https://source1.com)
        - [Recommendation 2 (ex:- drink water)](https://source2.com)
        - [Recommendation 3 (ex:- eat healthy)](https://source3.com)
        ''',
        agent=health_advisor,
    )

    return [analyze_blood_test, search_for_articles, provide_recommendations]