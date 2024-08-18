# Medical Report Analysis

This project analyzes blood test reports using AI agents to provide health recommendations and relevant articles.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/BishalJena/Blood_Analyzer.git
   cd medical-report-analysis
   ```
2. Setup virtual environment
   ```bash

   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys:

   ```bash
      touch .env
   ```

   Add your keys in .env file:
   ```
   SERPER_API_KEY=your_serper_api_key
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL_NAME=gpt-4o-mini
   OPENAI_API_BASE=https://api.openai.com/v1
   ```
4. To run the application, use the following command:

   ```bash
   streamlit run main.py
   ```

This will start the Streamlit server and open the application in your default web browser. Upload a PDF blood test report and click "Analyze Report" to get the analysis results.

## Project Structure

- `main.py`: The main Streamlit application.
- `agents.py`: Defines the AI agents used in the analysis.
- `tasks.py`: Defines the tasks performed by the agents.
- `utils.py`: Utility functions for the application.
- `.env`: Contains environment variables (API keys).
- `requirements.txt`: Lists the Python packages required for the project.

## How It Works

1. The user uploads a PDF blood test report.
2. The application extracts text from the PDF.
3. AI agents analyze the report, search for relevant articles, and provide health recommendations.
4. The results are displayed in a formatted manner within the Streamlit interface.