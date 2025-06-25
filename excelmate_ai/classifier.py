import os
import pandas as pd  # type: ignore
import groq  # type: ignore
import json
import re
import pdfplumber  # type: ignore
import docx  # type: ignore
import time

# Initialize Groq client
groq_client = groq.Client("Your API key")  # Replace with your key

# -------------------------
# File Reading & Extraction
# -------------------------

def load_data(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.csv':
        return pd.read_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        return pd.read_excel(file_path, engine='openpyxl')
    elif ext == '.pdf':
        return extract_tables_from_pdf(file_path)
    elif ext == '.docx':
        return extract_table_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type.")

def extract_tables_from_pdf(file_path: str) -> pd.DataFrame:
    all_rows = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_rows.extend(table)

    if not all_rows:
        raise ValueError("No tables found in PDF.")

    header = all_rows[0]
    data = all_rows[1:]
    return pd.DataFrame(data, columns=header)

def extract_table_from_docx(file_path: str) -> pd.DataFrame:
    doc = docx.Document(file_path)
    all_data = []

    for table in doc.tables:
        for i, row in enumerate(table.rows):
            text = [cell.text.strip() for cell in row.cells]
            all_data.append(text)

    if not all_data:
        raise ValueError("No tables found in DOCX.")

    header = all_data[0]
    data = all_data[1:]
    return pd.DataFrame(data, columns=header)

# ---------------------
# Classification Logic
# ---------------------

def extract_json(text: str):
    try:
        json_pattern = re.compile(r"\{(?:[^{}]|(?R))*\}", re.DOTALL)
        match = json_pattern.search(text)
        return json.loads(match.group()) if match else None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None

def build_prompt(row: pd.Series, categories: list, instructions: str) -> str:
    row_data = "\n".join([f"{col}: {val}" for col, val in row.items()])
    cat_text = "\n".join([f'- "{cat}"' for cat in categories])

    return f"""
You are an expert education data classifier.

Classify the student record below according to the user’s instruction.

Instructions:
{instructions}

Possible Categories:
{cat_text}

Respond ONLY in this JSON format (no explanation outside it):
{{
  "category": "CATEGORY_NAME",
  "reason": "Brief explanation (max 1 sentence)"
}}

Record:
{row_data}
"""

def classify_row(row: pd.Series, categories: list, instructions: str):
    prompt = build_prompt(row, categories, instructions)

    for _ in range(3):
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=200
            )
            result = response.choices[0].message.content.strip()

            print("\n=== Prompt Sent ===")
            print(prompt)
            print("\n=== LLM Response ===")
            print(result)

            json_data = extract_json(result)

            if json_data:
                category = json_data.get("category", "Unknown")
                reason = json_data.get("reason", "No reason provided.")
                if category not in categories:
                    print(f"⚠️ Invalid category received: {category}")
                    return "Other", reason
                return category, reason
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

    return "Unknown", "Classification failed after retries."

def classify_dataset(df: pd.DataFrame, categories: list, instructions: str) -> pd.DataFrame:
    df[['Category', 'Reason']] = df.apply(
        lambda row: classify_row(row, categories, instructions),
        axis=1, result_type='expand'
    )
    return df

def save_to_excel(df: pd.DataFrame, output_path: str):
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"\n✅ Classification complete. Saved to: {output_path}")
