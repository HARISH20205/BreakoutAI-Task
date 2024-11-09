import streamlit as st
import pandas as pd
import logging
from data import get_data_sheets
from scrap import data_scrap
logging.basicConfig(level=logging.DEBUG)

st.title("Data Upload and Query Dashboard")

# Initialize session state variables if they don't exist
if 'show_upload' not in st.session_state:
    st.session_state.show_upload = False
if 'show_sheets' not in st.session_state:
    st.session_state.show_sheets = False

# Create two columns for the buttons
col1, col2 = st.columns(2)
# Place buttons in separate columns
with col1:
    if st.button("Upload File"):
        st.session_state.show_upload = True
        st.session_state.show_sheets = False
with col2:
    if st.button("Link Google Sheets"):
        st.session_state.show_sheets = True
        st.session_state.show_upload = False

def main():
    # When 'Upload File' button is pressed, show file uploader and prompt
    if st.session_state.show_upload:
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        file_description = st.text_input("Enter the Prompt for the uploaded file: ")
        submit_button = st.button("Submit File")

        if submit_button and uploaded_file is not None:
            # Read and display the uploaded file
            df = pd.read_csv(uploaded_file)
            st.write("Here is a preview of the uploaded file:")
            st.dataframe(df.head())  # Show preview of the file
            st.write(f"File Description: {file_description}")
        elif submit_button:
            st.error("Please upload a CSV file to proceed.")

    # When 'Link Google Sheets' button is pressed, show Google Sheets URL input and prompt
    elif st.session_state.show_sheets:
        google_sheets_url = st.text_input("Enter Google Sheets URL")
        sheets_description = st.text_input("Enter the prompt for the uploaded file: ")
        submit_button_sheets = st.button("Submit Google Sheets Link")

        if submit_button_sheets and google_sheets_url:
            try:
                df = get_data_sheets(google_sheets_url)
                st.write("Here is a preview of the data from Google Sheets:")
                st.dataframe(df.head())
                st.write(f"Google Sheets Description: {sheets_description}")
                                    
            except Exception as e:
                st.error(f"Error fetching Google Sheets data: {str(e)}")
        elif submit_button_sheets:
            st.error("Please enter a valid Google Sheets URL.")

if __name__ == "__main__":
    main()