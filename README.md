# Excelmate AI 🎙️📊

**Excelmate AI** is an intelligent voice-command-based tool for performing operations on Excel datasets. This project utilizes natural language classification to identify user commands and performs relevant actions on Excel files, making data interaction faster and hands-free.

##  Features

- 🔍 Classifies user text/voice input commands using AI
- 🧾 Reads and modifies Excel/CSV files dynamically
- 📦 Lightweight and easy to integrate with other tools
- 🧪 Comes with sample data for testing

## Project Strucutre

excelmate_ai_package/
│
├── excelmate_ai/
│   ├── app.py               # Main application entry
│   ├── classifier.py        # Command classification logic
│   ├── requirements.txt     # Project dependencies
│   └── sample_data.csv      # Sample dataset for testing
│
└── venv/                    # Virtual environment (optional)

**📚 Dependencies**

1. pandas
2. scikit-learn
3. nltk
4. joblib
(Installable via requirements.txt)

**⚙️ How to Set Up**

💡 Python 3.10 or higher recommended

1. Clone or extract the repository
   git clone https://github.com/yourusername/excelmate-ai.git
   cd excelmate-ai/excelmate_ai_package/excelmate_ai

2. Install dependencies
    pip install -r requirements.txt

3. Run the application
    python app.py

**💡 Future Enhancements**

1. Speech-to-text integration for full voice control

2. Dash/Flask-based web dashboard

3. Agentic AI for multi-step command chaining

