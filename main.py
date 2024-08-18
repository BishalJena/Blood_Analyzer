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

# def extract_text_from_pdf(uploaded_file):
#     text = ""
#     try:
#         reader = PdfReader(uploaded_file)
#         for page in reader.pages:
#             text += page.extract_text()
#     except Exception as e:
#         st.error(f"Error reading the PDF file: {e}")
#         logger.error(f"Error reading the PDF file: {e}")
#         return None
#     return text

# def display_results(results):
#     if not isinstance(results, list) or len(results) != 3:
#         st.error("Unexpected results format. Please check the analysis output.")
#         return

#     analysis, articles, recommendations = results

#     st.subheader("Blood Test Analysis")
#     st.markdown(analysis)

#     st.subheader("Relevant Articles")
#     st.markdown(articles)

#     st.subheader("Health Recommendations")
#     st.markdown(recommendations)

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
            researcher, health_advisor, webmd_finder = initialize_agents()
            tasks = initialize_tasks(researcher, health_advisor, webmd_finder, blood_test_text=text)

            # Form the crew and define the process
            crew = Crew(
                agents=[researcher, health_advisor, webmd_finder],
                tasks=tasks,
                process=Process.sequential
            )

            # Kick off the crew process with the extracted text
            with st.spinner("Processing..."):
                try:
                    result = crew.kickoff(inputs={"text": text})
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


# def main():
#     st.title("Medical Report Analysis ➕")

#     uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

#     if uploaded_file is not None:
#         # Extract text from PDF
#         blood_test_text = extract_text_from_pdf(uploaded_file)
#         if blood_test_text is None:
#             return

#         if st.button("Analyze Report"):
#             st.write("Analyzing the report... This may take a few minutes.")
#             logger.info("Report analysis started")

#             try:
#                 # Initialize agents and tasks
#                 researcher, health_advisor, webmd_finder = initialize_agents()
#                 tasks = initialize_tasks(researcher, health_advisor, webmd_finder, blood_test_text)

#                 # Create a Crew with the agents and tasks
#                 crew = Crew(
#                     agents=[researcher, health_advisor, webmd_finder],
#                     tasks=tasks
#                 )

#                 # Execute the tasks
#                 results = crew.kickoff()

#                 logger.info("Report analysis completed successfully")

#                 # Display results
#                 display_results(results)

#             except Exception as e:
#                 st.error(f"An error occurred during analysis: {str(e)}")
#                 logger.error(f"Error during analysis: {str(e)}", exc_info=True)

#     else:
#         st.write("Please upload a PDF file to begin analysis.")

# if __name__ == "__main__":
#     main()