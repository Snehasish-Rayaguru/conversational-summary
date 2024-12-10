# #!/usr/bin/env python
# # coding: utf-8

# # In[15]:


# from dotenv import load_dotenv
# import os
# import json
# import ast

# load_dotenv()

# api_key = os.getenv("GROQ_API_KEY")
# if api_key is None:
#     raise ValueError("GROQ_API_KEY is not set in the .env file.")


# # In[16]:


# from langchain_groq import ChatGroq

# llm = ChatGroq(
#     model="mixtral-8x7b-32768",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )

# def extract_json(content):
#     start = content.find('```json\n') + 7
#     end = content.find('```', start)
#     json_str = content[start:end].strip()
#     return ast.literal_eval(json_str)
# def extract_json_manual(content):
#     start = content.find('```json\n') + 7
#     end = content.find('```', start)
#     json_str = content[start:end].strip()
#     import json 
#     return json.loads(json_str)

# def get_ai_msg(patient_prompt):
#     messages = messages = [  
#     {
#         "role": "system",
#         "content": """
#         You are a medical assistant capable of extracting structured details from unstructured clinical text provided by a doctor. Your task is to identify specific categories of information from the provided text precisely. Additionally, you need to identify and flag any unknown or unfamiliar terms that may need further clarification or special handling.

#         The categories you need to extract from the text are:
#         1. **Status**: Identify the patient's health status, such as "stable," "critical," "recovering," "improving," etc.
#         2. **Pharmacy**: Extract references to medication, prescriptions, or pharmacy-related details (e.g., medication names, dosages, directions).
#         3. **Services**: Extract any references to medical services, tests, or procedures mentioned (e.g., lab tests, imaging, surgeries).
#         4. **Unknown Words**: Flag any terms or phrases that are unfamiliar or do not fit within the recognized categories, indicating the need for further clarification or special handling.

#         Please note that further clarification or special handling may be needed for the patient's health status and the interpretation of their symptoms.
#         """
#     },
#     {
#         "role": "system",
#         "content": """
#         Based on the provided information, respond strictly in valid JSON format enclosed in triple backticks (`json`). Use the following schema:

#         ```json
#         {
#             "status": "stable",  // Replace with identified status.
#             "pharmacy": {
#                 "medications": [
#                     {
#                         "name": "medicine name",  // Replace with actual medication name.
#                         "dosage": "dosage amount",  // Replace with dosage.
#                         "unit": "unit",  // Replace with unit (e.g., mg, ml).
#                         "ICD_code": "ICD code",  // Search and include the ICD code.
#                         "frequency": "frequency details"  // Replace with specific time periods (e.g., daily, twice a day).
#                     }
#                 ]
#             },
#             "services": {  
#                 "tests": [
#                     // Include all prescribed tests, if any.
#                 ]           
#             },
#             "unknown_words": [ 
#                 // Include any unfamiliar or unclear terms.
#             ]
#         }
#         ```

#         Ensure the response strictly adheres to this JSON schema.
#         """
#     },
#     {
#         "role": "user",
#         "content": patient_prompt
#     }
# ]

#     ai_msg = llm.invoke(messages)
#     ai_msg_json=extract_json(ai_msg.content)
#     ai_msg_json= extract_json_manual(ai_msg.content)
#     ai_msg_json_file = json.dumps(ai_msg_json, indent=4)
#     return ai_msg_json_file

# def get_ai_msg_manual(patient_prompt):
#     return get_ai_msg(patient_prompt)
