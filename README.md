# MCQ Generator with LangChain & Streamlit

This project is an interactive web application for generating and practicing Multiple Choice Questions (MCQs) from PDF or text files using OpenAI's GPT models and LangChain. The app allows users to upload study material, generate MCQs, answer them, and receive instant feedback and explanations.

## Features
- Upload PDF or TXT files as study material
- Automatically generate MCQs using OpenAI's GPT-3.5/4 via LangChain
- Interactive quiz interface: select answers, submit, and get instant feedback
- Explanations and review for each question
- Score summary and ability to restart the quiz

## Tech Stack & Libraries
- **Python 3.8+**
- **Streamlit**: For the web UI
- **LangChain**: For LLM orchestration
- **OpenAI**: For GPT-3.5/4 API access
- **PyPDF2**: For PDF file reading
- **python-dotenv**: For environment variable management
- **pandas**: For tabular data handling

### Python Packages Used
- `streamlit`
- `langchain`
- `langchain-openai`
- `langchain-community`
- `openai`
- `PyPDF2`
- `python-dotenv`
- `pandas`

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd MCQ_generator
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

5. **Run the Streamlit app**
   ```bash
   streamlit run StreamlitAPP.py
   ```
   The app will open in your browser at `http://localhost:8501`.

## Usage
1. Upload a PDF or TXT file containing study material.
2. Enter the number of MCQs, subject, and desired complexity/tone.
3. Click **Create MCQs** to generate the quiz.
4. Select your answers for each question.
5. Click **Submit Answers** to see your score, correct answers, and explanations.
6. Use **Start Over** to reset and try again with new material or settings.

## File Structure
- `StreamlitAPP.py` — Main Streamlit app
- `src/mcq_generator/MCQGenerator.py` — MCQ generation logic using LangChain & OpenAI
- `src/mcq_generator/utils.py` — File reading and quiz data utilities
- `Response.json` — Example MCQ JSON structure
- `requirements.txt` — All required Python packages
- `README.md` — This file

## Notes
- Make sure your OpenAI API key has sufficient quota.
- The app is designed for educational and demo purposes.
- For best results, use clear and well-structured study material.

## License
MIT License
