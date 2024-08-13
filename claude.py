from anthropic import AnthropicVertex
from dotenv import load_dotenv
import os, json

# Set up your location and project ID
load_dotenv()
LOCATION = os.getenv("LOCATION") or "us-east5"
PROJECT_ID = os.getenv("PROJECT_ID") or "your-project-id"

# Initialize the chat history
chat_history = []

# Initialize the client
client = AnthropicVertex(region=LOCATION, project_id=PROJECT_ID)

# Function to send a message and get a response
def send_message(user_input):
    # Add the user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Send the message with the entire chat history
    response = client.messages.create(
        max_tokens=4096,
        messages=chat_history,
        model="claude-3-5-sonnet",
    )

    # Extract text from each TextBlock in the response
    assistant_response = " ".join([block.text for block in response.content])

    # Add the response to the chat history
    chat_history.append({"role": "assistant", "content": assistant_response})

    # Return the assistant's response content
    return assistant_response

def conversation_runner():
    print("Enter your message (type 'END' on a new line to send):")
    
    while True:
        print("You: ", end="")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        
        user_input = "\n".join(lines)
        
        # End convo
        if user_input.lower() in ["exit", "quit", "bye"]:
            title = send_message("Ignore all previous instructions. The preceding text is a conversation thread that needs a concise but descriptive 3 to 5 word title in natural English so that readers will be able to easily find it again. Do not add any quotation marks or formatting to the title. Respond only with the title text.")
            with open(f'{title}-history.json', 'w') as json_file:
                json.dump(chat_history[:-2], json_file)
            break
            
        response = send_message(user_input)
        print(f"Claude: {response}")

def main():
    files = [f for f in os.listdir() if f.endswith('-history.json')]
    if files:
        print("Select a file to load:")
    
        print("0. Start a new conversation")
    
        for i, file in enumerate(files, 1):
            print(f"{i}. {file.replace('-history.json', '')}")
    
        choice = int(input("Enter the number of the file you want to load: "))
        if choice == 0:
            pass
        else:
            choice = choice - 1
            selected_file = files[choice]
            chat_history = json.load(open(selected_file))
            for message in chat_history:
                print(f"{message['role'].capitalize()}: {message['content']}")
    
    # Start the conversation
    conversation_runner()
    
if __name__ == "__main__":
    main()