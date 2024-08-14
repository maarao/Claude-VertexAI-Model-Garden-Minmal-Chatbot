from flask import Flask, request, jsonify
from flask_cors import CORS
from claude import send_message

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']

    # Here, you would typically call your LLM to generate a response
    # For this example, we'll just echo the user's message
    bot_response = send_message(user_message)

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)