from flask import Flask, request, render_template
import pandas as pd
import json
import ast
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Groq API key
api_key = os.getenv("GROQ_API_KEY")
if api_key is None:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

# Initialize ChatGroq
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def extract_json(content):
    start = content.find('```json\n') + 7
    end = content.find('```', start)
    json_str = content[start:end].strip()
    return ast.literal_eval(json_str)

def extract_json_manual(content):
    start = content.find('```json\n') + 7
    end = content.find('```', start)
    json_str = content[start:end].strip()
    return json.loads(json_str)

def get_ai_msg(patient_prompt):
    messages = [
        {
            "role": "system",
            "content": """
            You are a medical assistant tasked with extracting specific details from the given clinical passage. 
            Extract the following categories:
            1. **Major Problems**: The diseases or conditions the patient is suffering from.
            2. **Medicines**: The medications prescribed by the doctor for the patient.
            3. **Doctor Instructions**: Instructions or advice provided by the doctor for the patient to follow.
            4. **Content Summary**: A concise summary of the entire passage in 3 to 5 lines.

            Respond strictly in valid JSON format enclosed in triple backticks (`json`) using this schema:
            ```json
            {
                "major_problems": ["list of diseases or conditions"],
                "medicines": [
                    {
                        "name": "medicine name",
                        "dosage": "dosage",
                        "unit": "unit",
                        "frequency": "frequency"
                    }
                ],
                "doctor_instructions": ["list of instructions"],
                "content_summary": "summary text"
            }
            ```
            Ensure the response strictly adheres to this schema.
            """
        },
        {
            "role": "user",
            "content": patient_prompt
        }
    ]

    ai_msg = llm.invoke(messages)
    ai_msg_json = extract_json_manual(ai_msg.content)
    return ai_msg_json

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    patient_prompt = request.form['patient_prompt']
    response = get_ai_msg(patient_prompt)

    # Extract data from the AI response
    major_problems = response.get("major_problems", [])
    medicines = response.get("medicines", [])
    doctor_instructions = response.get("doctor_instructions", [])
    content_summary = response.get("content_summary", "Not Available")

    # Process Medicines Section (table format)
    medicines_data = []
    for medicine in medicines:
        medicines_data.append({
            "Medicine": medicine.get("name", "N/A"),
            "Quantity": medicine.get("dosage", "N/A"),
            "Unit": medicine.get("unit", "N/A"),
            "Frequency": medicine.get("frequency", "N/A")
        })

    # Create DataFrame for Medicines
    medicines_df = pd.DataFrame(medicines_data)

    return render_template(
        'result.html',
        major_problems=major_problems,
        medicines=medicines_df.to_html(classes='table', index=False),
        doctor_instructions=doctor_instructions,
        content_summary=content_summary
    )

if __name__ == '__main__':
    app.run(debug=True)
