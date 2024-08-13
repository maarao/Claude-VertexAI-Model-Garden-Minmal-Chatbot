from anthropic import AnthropicVertex
from dotenv import load_dotenv
import os, json

# Set up your location and project ID
load_dotenv()
LOCATION = os.getenv("LOCATION") or "us-east5"
PROJECT_ID = os.getenv("PROJECT_ID") or "your-project-id"


# Initialize the client
client = AnthropicVertex(region=LOCATION, project_id=PROJECT_ID)

# Initialize the chat history
chat_history = []

# Function to send a message and get a response
def send_message(user_input):
    # Add the user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Send the message with the entire chat history
    response = client.messages.create(
        max_tokens=1024,
        messages=chat_history,
        model="claude-3-5-sonnet",
    )
    
    # Extract text from each TextBlock in the response
    assistant_response = " ".join([block.text for block in response.content])
    
    # Add the response to the chat history
    chat_history.append({"role": "assistant", "content": assistant_response})
    
    # Return the assistant's response content
    return assistant_response

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        title = send_message("Ignore all previous instructions. The preceding text is a conversation thread that needs a concise but descriptive 3 to 5 word title in natural English so that readers will be able to easily find it again. Do not add any quotation marks or formatting to the title. Respond only with the title text.")
        with open(f'{title}-history.json', 'w') as json_file:
            json.dump(chat_history[:-2], json_file)
        break
    response = send_message(user_input)
    print(f"Claude: {response}")
