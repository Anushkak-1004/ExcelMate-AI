# Excelmate AI 🎙️📊

**Excelmate AI** is an intelligent voice-command-based tool for performing operations on Excel datasets. This project utilizes natural language classification to identify user commands and performs relevant actions on Excel files, making data interaction faster and hands-free.

---

## 🧠 Features

- 🔍 Classifies user text/voice input commands using AI  
- 🧾 Reads and modifies Excel/CSV files dynamically  
- 📦 Lightweight and easy to integrate with other tools  
- 🧪 Comes with sample data for testing

---

## 🏗️ Project Structure

```text
excelmate_ai_package/
│
├── excelmate_ai/
│   ├── app.py               # Main application entry
│   ├── classifier.py        # Command classification logic
│   ├── requirements.txt     # Project dependencies
│   └── sample_data.csv      # Sample dataset for testing
│
└── venv/                    # Virtual environment (optional)```


## ⚙️ How to Set Up
'''text
> 💡 **Python 3.10 or higher** recommended```

### 1. Clone or extract the repository

```bash
git clone https://github.com/yourusername/excelmate-ai.git
cd excelmate-ai/excelmate_ai_package/excelmate_ai```

.### 2. Install dependencies

```bash
pip install -r requirements.```

### 3.  Run the application

```bash
   python app.py```

**🧪 Sample Usage**
Modify sample_data.csv or replace it with your own CSV file.

Then run the app and input a natural command such as:

"Add a column named 'GPA'"
"Update the value in row 3 column 'Grade' to 'A'"

The classifier.py handles understanding your intent, and app.py performs the data operation.

📚 Dependencies
- `pandas`
-`scikit-learn`
-`nltk`
-`joblib`
(Installable via requirements.txt)

💡 Future Enhancements
-`Speech-to-text integration for full voice control`

-`Dash/Flask-based web dashboard`

-`Agentic AI for multi-step command chaining`





