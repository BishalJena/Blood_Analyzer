import os
import PyPDF2  # For reading PDFs
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from tabulate import tabulate  # For table formatting

# Function to read and extract text from the PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

# Path to the blood test report (adjusted for your environment)
pdf_path = 'final/sample_report.pdf'

# Extracted text from the PDF
blood_test_text = extract_text_from_pdf(pdf_path)

# Define LLM (Ollama)
ollama_openhermes = Ollama(model="openhermes")
os.environ['SERPER_API_KEY'] = "5fc477693c562ed17221137ed4dacfa7133fa189"
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
    description='Find four relevant WebMD articles based on the health recommendations provided.',
    agent=webmd_finder,
    expected_output="List of four relevant WebMD articles"
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

# Limit the WebMD articles to 4
def limit_articles(webmd_articles):
    limited_articles = []
    counter = 0
    for article in webmd_articles.split('\n'):
        if article.strip():
            limited_articles.append(article.strip())
            counter += 1
        if counter == 4:
            break
    return limited_articles

# Function to format output in table format
def format_output(summary, recommendations, webmd_articles):
    summary_table = [["Parameter", "Value"]] + [line.split(':') for line in summary.split('\n') if line.strip()]
    recommendations_table = [["Health Recommendations"]] + [[rec.strip()] for rec in recommendations.split('\n') if rec.strip()]
    articles_table = [["Relevant WebMD Articles"]] + [[article.strip()] for article in limit_articles(webmd_articles)]

    print("====================================")
    print(tabulate(summary_table, headers="firstrow", tablefmt="grid"))
    print("\n====================================")
    print(tabulate(recommendations_table, headers="firstrow", tablefmt="grid"))
    print("\n====================================")
    print(tabulate(articles_table, headers="firstrow", tablefmt="grid"))
    print("\n====================================")

# Format and print the output
format_output(summary, recommendations, webmd_articles)
