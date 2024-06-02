from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

# Load the conversational pipeline from Hugging Face Transformers
nlp = pipeline("conversational")

conversation_history = []

basic_questions = {
    "how are you": "I'm a bot, so I don't have feelings, but thanks for asking!",
    "what is your name": "I'm a simple chatbot created for this project.",
    "what can you do": "I can chat with you and remember some context from our conversation.",
    "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "what's the weather like": "I'm not connected to the internet, so I can't check the weather right now."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    user_input = user_input.lower()

    # Add user input to conversation history
    conversation_history.append(("User", user_input))
    
    response = basic_questions.get(user_input)
    if not response:
        response = generate_response(user_input)

    # Add bot response to conversation history
    conversation_history.append(("Bot", response))
    
    return jsonify({"response": response})

def generate_response(user_input):
    try:
        conversation = nlp(user_input)
        if conversation:
            return conversation[0]['generated_text']
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return "I'm not sure how to respond to that."

@app.route('/context')
def context():
    return jsonify({"conversation_history": conversation_history})

if __name__ == '__main__':
    app.run(debug=True)
