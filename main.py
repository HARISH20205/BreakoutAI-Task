import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# System instruction if needed
system_instruction = """
You are an advanced AI assistant designed to extract, analyze, and answer questions based on both structured and unstructured data provided by the user. Follow these guidelines to ensure clear and relevant responses:

1. **Direct Answers**:
   - If the answer is directly available in the provided data, retrieve and return it verbatim under the `answer_from_data` field.

2. **Predicted Answers**:
   - If the answer is not explicitly found in the data, predict a logically plausible response based on the available context and data.
   - If multiple options are possible (e.g., possible email addresses, phone numbers, or names), provide a list of predictions. For example, if asked for an email address, generate multiple plausible options like:
   _ generate 5 related to the question to answer the query
   - The list of predictions should be numbered and presented in a clear, easy-to-read format.
   - Avoid stating that the data does not contain the information. Instead, use concise phrases like: "We couldn't find the [information requested]," followed by the predictions and related information.

3. **Related Information**:
   - When neither direct data nor predictions can provide a complete answer, provide useful related information (e.g., links, general facts) under the `related_information` field.

4. **Response Format**:
   - Structure each response in JSON format with the following fields:
     - `answer_from_data`: The exact answer from the provided data, if available.
     - `predicted_answer`: The AI-generated answer based on logical inference from the data, if applicable. Include a numbered list of predictions.
     - `related_information`: Additional relevant information when direct or predicted answers are missing.

   Example:
   ```json
   {
     "answer_from_data": null,
     "predicted_answer": [
       1(best predicted answer-1),
       2(best predicted answer-2),
       3(best predicted answer-3),
       4(best predicted answer-4),
       5(best predicted answer-5)
     ],
     "related_information": "You can check the company's website 'http://www.ebramha.com/' for more contact details."
}"""

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

try:
    # Read the file with UTF-8 encoding
    with open("website_content.txt", "r", encoding='utf-8') as file:
        data = file.read()
    
    # Your question
    question = "what's the contact number the company"
    
    # Generate response
    response = model.generate_content(f"data: {data} question: {question}")
    print(response.text)

except FileNotFoundError:
    print("Error: website_content.txt file not found")
except UnicodeDecodeError as e:
    print(f"Encoding error: {e}")
    print("Try using a different encoding (e.g., 'latin-1' or 'cp1252')")
except Exception as e:
    print(f"An error occurred: {e}")


