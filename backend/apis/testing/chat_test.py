import requests
import json

# Define the API endpoint
api_url = "http://127.0.0.1:5000/api/next_question"

# Initialize chat history
chat_history = ""

def get_next_interaction(chat_history):
    # Make the API request
    response = requests.post(api_url, json={"chat_history": chat_history})
    
    # Parse the response
    if response.status_code == 200:
        data = response.json()
        next_interaction = data.get("next_interaction")
        final_report = data.get("final_report")
        return next_interaction, final_report
    else:
        print("Error:", response.status_code, response.text)
        return None, False

def conversation_loop():
    global chat_history
    while True:
        # Get the next interaction from the API
        next_interaction, final_report = get_next_interaction(chat_history)
        
        if next_interaction:
            # Print the next interaction
            print(next_interaction)
            
            if final_report:
                print("Final Report:")
                print(next_interaction)
                break
            
            # Get user input
            user_input = input("You: ")
            
            # Update chat history
            chat_history += f"\nPatient: {user_input}\nAgent: {next_interaction}"
        else:
            print("Failed to get a response from the API.")
            break

if __name__ == "__main__":
    conversation_loop()
