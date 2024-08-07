from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import google.generativeai as genai

GOOGLE_API_KEY = 'GOOGLE_API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the LLM model
llm = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Define the detailed instructions for the message
detailed_instructions = """
Assess the following health indicators based on the visual input from the provided video of the patient:

Skin Color and Condition:
1. Pale skin (anemia, shock, low oxygen)
2. Yellowish skin (jaundice, liver issues)
3. Blue skin/lips (cyanosis, poor oxygenation)
4. Redness (infection, inflammation, allergy)
5. Rashes/hives (allergic reaction, infection, eczema)
6. Pimples/pustules/pox (infection like chickenpox, measles, acne)
7. Heavy sweating (fever, anxiety)

Eyes:
1. Dark circles (sleep deprivation, stress, fatigue)
2. Yellowing (scleral icterus, jaundice, liver issues)
3. Red/bloodshot eyes (infection, allergy, irritation)
4. Drooping eyelids (ptosis, neurological issues, fatigue)

Mouth and Lips:
1. Blue lips (cyanosis, poor oxygenation)
2. Swollen lips (allergic reaction, infection)
3. Cracked/dry lips (dehydration, vitamin deficiency)

Neck Region:
1. Swollen glands (infection, immune response)
2. Visible thyroid enlargement (goiter, thyroid disorder)

Additional Observations:
1. Seizures (uncontrollable shaking, convulsions)
2. Difficulty breathing (labored, rapid breathing)
3. Visible swelling (hands, legs, face)
4. Deep cuts/wounds (require immediate attention)
5. Posture and movement (pain, discomfort, neurological issues)
6. Tremors (involuntary shaking)

return every symptom you observe in the patient with analysis. If you do not observe any symptoms, please state that clearly.
"""

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Upload the file to the model
        uploaded_file = genai.upload_file(file_path)
        
        # Generate the content based on the uploaded file and detailed instructions
        response = llm.generate_content([uploaded_file, detailed_instructions])
        
        # Delete the file after processing
        os.remove(file_path)

        # Return the result
        return jsonify({"result": response.text})

if __name__ == '__main__':
    app.run(debug=True)
