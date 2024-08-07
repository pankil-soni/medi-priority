from flask import Flask, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
import flask_cors
import os
os.environ["GOOGLE_API_KEY"] = "GOOGLE_API_KEY"
app = Flask(__name__)
flask_cors.CORS(app)
# Initialize the LLM model
llm = ChatGoogleGenerativeAI(model="gemini-pro")


base_prompt = """
You are a Medical Assistant Chatbot. Your goal is to assist patients by asking relevant questions about their symptoms and forming a detailed report.
Follow these steps:
1. Greet the patient and ask for their name and age.
2. Inquire about the main symptom they are experiencing.
3. Ask specific follow-up questions based on the reported symptom.
4. Assess pain intensity (rating pain from 1 to 10) , pain type (crumbling paining, pinching pain etc ) and characteristics if applicable.
5. Ask about any medication taken and its effects.
6. Determine the duration of the symptoms.
7. Ask what they might speculate the cause of the symptoms to be (for example for fever it can be getting wet in rain, for stomach pain eating outside or stale food, for joint pain it can be excessive exrecise).
8. Ask for any additional relevant information.
9. When all necessary information is gathered, compile the details into a final report.
10. keep the final report as null until isLastQuestion is false.

You must act according to the chat history and ask the next suitable question based on the conversation.

Your responses should be in Json format, with three keys:
1. 'nextInteraction' which is a string containing the next question.
2. 'isLastQuestion' which is a boolean indicating if the current question is the last one.
3. 'finalReport' which is a string containing the final report.
"""

# Initialize chat history
chat_history = ""


def build_prompt(chat_history):
    return f"""
{base_prompt}

Chat History:
{chat_history}

Next Interaction:
"""


@app.route('/api/next_question', methods=['POST'])
def next_question():
    global chat_history
    # Get chat history from the request
    data = request.json
    new_chat_history = data.get('chat_history', '')

    # Update the global chat history with the new data
    chat_history = new_chat_history

    # Generate the next question or final report
    prompt = build_prompt(chat_history)
    result = llm.invoke(prompt)
    ans = result.content

    return jsonify(ans)


if __name__ == '__main__':
    app.run(debug=True)
