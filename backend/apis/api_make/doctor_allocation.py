from flask import Flask, request, jsonify
from crewai import Agent, Task, Crew
import os
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)

# Set up the environment variable for Google API Key
os.environ["GOOGLE_API_KEY"] = "REMOVED"

# Initialize the LLM model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Define the agent and task
assigning_doctor_agent = Agent(
    role="To assign a doctor to the patient based on the symptoms",
    goal="To assign a doctor to the patient based on the symptoms",
    backstory="You have general information about a patient and also the visual symptoms of the patient. You need to assign a doctor to the patient based on the symptoms.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

assign_doctor_task = Task(
    description=(
        "1. You have a list of doctors and their specializations which is {doctor_list}.\n"
        "2. You have the general information about patient {general_information} .\n"
        "3. You also have the visual symptoms of the patient which is {visual_symptoms}.\n"
        "4. You need to assign a doctor to the patient based on the symptoms."
        "5. Only provide the type of the doctor assigned to the patient in plain text with no additional text."
    ),
    expected_output="The type of the doctor assigned to the patient",
    agent=assigning_doctor_agent
)

doctor_list = """
1. MBBS - General Physician
2. MD - Dermatologist
3. ENT Specialist
4. Physiotherapist
5. Cardiologist
6. Neurologist
7. Oncologist
8. Pediatrician
9. Orthopedic Surgeon
10. Psychiatrist
"""

@app.route('/api/assign_doctor', methods=['POST'])
def assign_doctor():
    data = request.get_json()
    general_information = data.get('general_information')
    visual_symptoms = data.get('visual_symptoms')

    inputs = {
        "doctor_list": doctor_list,
        "general_information": general_information,
        "visual_symptoms": visual_symptoms
    }

    crew = Crew(agents=[assigning_doctor_agent], tasks=[assign_doctor_task], verbose=2)
    result = crew.kickoff(inputs)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
