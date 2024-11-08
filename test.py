import streamlit as st
import pandas as pd

def main():
    st.title("User Interface Prompt for Data Upload and Query Dashboard")

    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    # Place buttons in separate columns
    with col1:
        upload_file_button = st.button("Upload File")
    with col2:
        link_google_sheets_button = st.button("Link Google Sheets")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    google_sheets_url = st.text_input("Enter Google Sheets URL")
    
    if upload_file_button and uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df.head())
        main_column = st.selectbox("Select the main column", df.columns)
    
    if link_google_sheets_button and google_sheets_url:
        sheet_id = google_sheets_url.split("/")[5]
        sheet_name = "Sheet1"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        st.write("Data Preview:")
        st.dataframe(df.head())
        main_column = st.selectbox("Select the main column", df.columns)

    # Query input
    query_template = st.text_input("Enter your query template (use {placeholder} for dynamic values)")
    if query_template and 'df' in locals() and main_column:
        sample_value = df[main_column].iloc[0]
        sample_query = query_template.replace("{company}", sample_value)
        st.write("Sample Query:")
        st.write(sample_query)

if __name__ == "__main__":
    main()