import requests
import os

API_URL = "http://127.0.0.1:5000/api/analyze"
UPLOAD_FILE_PATH = "img1.jpg"  # Replace with the actual path

def upload_file(file_path):
    with open(file_path, 'rb') as file:
        response = requests.post(API_URL, files={'file': file})
    return response.json()

def main():
    chat_history = []

    while True:
        # Upload the file and get the response
        response = upload_file(UPLOAD_FILE_PATH)
        print("Response from API:", response['result'])

        # Ask for user input to continue the chat
        user_input = input("Enter your input (type 'exit' to stop): ")
        if user_input.lower() == 'exit':
            break

        # Maintain the chat history
        chat_history.append({"user": user_input, "response": response['result']})

        # Print the chat history
        print("\nChat History:")
        for chat in chat_history:
            print(f"User: {chat['user']}\nResponse: {chat['response']}\n")

if __name__ == "__main__":
    main()
