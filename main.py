import os
import PyPDF2  # For reading PDFs
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Function to read and extract text from the PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

# Path to the blood test report (adjusted for your environment)
pdf_path = 'Blood_Analyzer/sample_report.pdf'

# Extracted text from the PDF
blood_test_text = extract_text_from_pdf(pdf_path)

# Define LLM (Ollama)
ollama_openhermes = Ollama(model="openhermes")

# INSERT YOUR SERPER API KEY
os.environ['SERPER_API_KEY'] = "YOUR_API_KEY"
# Initialize Serper search tool
serper_search_tool = SerperDevTool()

# Define Agents
researcher = Agent(
    role='Researcher',
    goal='Analyze the blood test report and give the data with values of all blood parameters in an organized table format.',
    backstory='You are an AI medical assistant specializing in analyzing blood test reports and presenting the data with detailed levels/data of each parameter.',
    verbose=True,
    allow_delegation=False,
    llm=ollama_openhermes
)

health_advisor = Agent(
    role='Health Advisor',
    goal='Provide health recommendations based on the blood test report summary, formatted in an organized table for easy readability.',
    backstory='You are an AI health advisor specializing in giving personalized health recommendations based on detailed analysis of blood reports.',
    verbose=True,
    allow_delegation=False,
    llm=ollama_openhermes
)

webmd_finder = Agent(
    role='WebMD Finder',
    goal='Find four relevant WebMD articles based on the health recommendations provided.',
    backstory='You are an AI assistant specializing in finding accurate and relevant WebMD articles based on health advice provided.',
    verbose=True,
    allow_delegation=False,
    llm=ollama_openhermes,
    tools=[serper_search_tool]  # Add the Serper search tool
)

# Define Tasks
task1 = Task(
    description=f'Analyze the following blood test report and provide a detailed summary with values of all blood parameters: {blood_test_text}',
    agent=researcher,
    expected_output="Summary of the blood test report with detailed values"
)

task2 = Task(
    description='Based on the blood test summary, provide health recommendations to improve health status.',
    agent=health_advisor,
    expected_output="Health recommendations based on the blood test summary"
)

task3 = Task(
    description='Find relevant WebMD articles based on the health recommendations provided.',
    agent=webmd_finder,
    expected_output="List of relevant WebMD articles"
)

# Define the Crew
crew = Crew(
    agents=[researcher, health_advisor, webmd_finder],
    tasks=[task1, task2, task3],
    verbose=True,  # Set verbose to True for detailed output
    process=Process.sequential
)

# Run the Crew
result = crew.kickoff()

# Extract results from the output
summary = result.task_results[0].output
recommendations = result.task_results[1].output
webmd_articles = result.task_results[2].output

# Function to format output
def format_output(summary, recommendations, webmd_articles):
    print("====================================")
    print("Blood Test Summary:")
    print(summary)
    print("\n====================================")
    print("Health Recommendations:")
    print(recommendations)
    print("\n====================================")
    print("Relevant WebMD Articles:")
    print(webmd_articles)
    print("\n====================================")

# Format and print the output
format_output(summary, recommendations, webmd_articles)
