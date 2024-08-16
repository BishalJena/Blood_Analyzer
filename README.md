# Blood_Analyzer
Certainly! Below is a GitHub README file that includes instructions for installing prerequisites, setting up the `openhermes` model on Ollama, and running the `main.py` script.

---

# Blood Test Report Analyzer and Health Advisor

This project utilizes AI to analyze a blood test report, provide health recommendations, and find relevant WebMD articles. The system is powered by multiple AI agents working together using the Ollama `openhermes` model and Serper search tool.

Here's video of the output:
(YouTube Link)[https://youtu.be/4o3mmO95HTo]

## Prerequisites

### 1. Install Required Python Libraries

Ensure that you have Python 3.8 or higher installed. Install the required libraries by running the following command:

```bash
pip install PyPDF2 langchain_community crewai crewai_tools
```

### 2. Set Up Ollama and the `openhermes` Model

You need to set up Ollama and ensure that the `openhermes` model is available:

1. **Install Ollama**:
   - Follow the installation instructions from the [Ollama website](https://ollama.com/download) to set up Ollama on your machine.

2. **Download the `openhermes` Model**:
   - Once Ollama is installed, download the `openhermes` model by running the following command in your terminal:

   ```bash
   ollama run openhermes
   ```

### 3. Get a Serper API Key

To use the Serper search tool, you need an API key:

1. Sign up for Serper API at [serper.dev](https://serper.dev/).
2. After obtaining your API key, insert it into the environment variable in the script:

```python
os.environ['SERPER_API_KEY'] = "YOUR_API_KEY"
```

Replace `"YOUR_API_KEY"` with your actual API key.

## Usage

### 1. Set Up Your Blood Test Report

Ensure you have your blood test report in PDF format. Update the path to your PDF in the script:

```python
pdf_path = 'Blood_Analyzer/sample_report.pdf'
```

Change `'Blood_Analyzer/sample_report.pdf'` to the path where your PDF is stored.

### 2. Run the Script

After setting up everything, run the script using the following command:

```bash
python main.py
```
or
```bash
python3 main.py
```
### 3. View the Output

The script will output:

- A summary of the blood test report with detailed values.
- Health recommendations based on the report.
- A list of relevant WebMD articles.
