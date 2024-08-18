import logging
from dotenv import load_dotenv
import streamlit as st
from crewai import Crew, Process
from pypdf import PdfReader
from agents import initialize_agents
from tasks import initialize_tasks

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("Medical Report Analysis ➕")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Extract text from PDF
        text = ""
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text()
        except Exception as e:
            st.error(f"Error reading the PDF file: {e}")
            logger.error(f"Error reading the PDF file: {e}")
            return

        if st.button("Analyze Report"):
            st.write("Analyzing the report... This may take a few minutes.")
            logger.info("Report analysis started")

            # Initialize agents and tasks
            medical_analyst, health_researcher, health_advisor = initialize_agents()
            tasks = initialize_tasks(medical_analyst, health_researcher, health_advisor, blood_test_text=text)

            # Form the crew and define the process
            crew = Crew(
                agents=[medical_analyst, health_researcher, health_advisor],
                tasks=tasks,
                process=Process.sequential
            )

            # Kick off the crew process with the extracted text
            with st.spinner("Processing..."):
                try:
                    result = crew.kickoff()
                    logger.info("Report analysis completed successfully")
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
                    logger.error(f"An error occurred during analysis: {e}")
                    return

            # Display results using Markdown for word wrapping and clickable links
            st.subheader("Analysis Results")
            st.markdown(result)
    else:
        st.write("Please upload a PDF file to begin analysis.")

if __name__ == "__main__":
    main()