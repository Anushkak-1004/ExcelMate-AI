import streamlit as st # type: ignore
import pandas as pd # type: ignore
import tempfile
from io import BytesIO
import plotly.express as px # type: ignore
from classifier import load_data, classify_dataset

# Page settings
st.set_page_config(page_title="EXCELMATE AI", layout="wide")
st.title("🤖 EXCELMATE AI - Universal Data Classifier")

st.markdown("""
Welcome to your intelligent data assistant! 

- Upload **any file** (`.csv`, `.xlsx`, `.pdf`, `.docx`)
- Define **custom categories and rules**
- Let the **LLM classify** each row intelligently
""")

# File uploader
uploaded_file = st.file_uploader("📁 Upload your file", type=["csv", "xlsx", "pdf", "docx"])

if uploaded_file:
    try:
        # Save uploaded file to a temp file to get its path
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        df = load_data(temp_path)

        st.success(" File loaded successfully!")
        st.subheader(" Preview of Uploaded Data")
        st.dataframe(df.head())

        with st.expander(" Define Your Classification Categories"):
            category_input = st.text_area("Enter categories (one per line):", height=150)
            categories = [cat.strip() for cat in category_input.splitlines() if cat.strip()]

        instructions = st.text_area(" Enter classification instructions for the AI:")

        if st.button(" Classify Data") and categories and instructions:
            with st.spinner("Classifying... this may take a few seconds depending on data size"):
                df_classified = classify_dataset(df, categories, instructions)

            st.success("Classification complete!")
            st.subheader("Classified Data")
            st.dataframe(df_classified)

            # Visualization
            st.subheader(" Category Distribution")
            fig = px.pie(df_classified, names="Category", title="Distribution by Category")
            st.plotly_chart(fig)

            # Download button
            output = BytesIO()
            df_classified.to_excel(output, index=False, engine="openpyxl")
            st.download_button(
                label=" Download Classified File",
                data=output.getvalue(),
                file_name="classified_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f" Error: {e}")
