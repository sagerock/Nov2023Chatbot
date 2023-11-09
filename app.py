from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_random_secret_key'  # Set this to a complex random value

# Load environment variables from .env file
load_dotenv()

DATA_FILE = 'data.json'

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/custom_prompt', methods=['POST'])
def create_or_update_prompt():
    data = request.json
    prompt_id = data.get('prompt_id')
    content = data.get('content')

    if not prompt_id or not content:
        return jsonify({'error': 'Invalid data'}), 400

    prompts = read_data()
    prompt = next((item for item in prompts if item['prompt_id'] == prompt_id), None)

    if prompt is None:
        prompts.append({'prompt_id': prompt_id, 'content': content})
    else:
        prompt['content'] = content

    write_data(prompts)

    return jsonify({'message': 'Prompt saved successfully', 'prompt_id': prompt_id}), 201

@app.route('/custom_prompt/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    prompts = read_data()
    prompt = next((item for item in prompts if item['prompt_id'] == prompt_id), None)
    if prompt:
        return jsonify(prompt), 200
    else:
        return jsonify({'error': 'Prompt not found'}), 404

# You will need to implement similar logic for PUT and DELETE methods to update and delete prompts

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    prompt_id = data.get('prompt_id')
    temperature = data.get('temperature', 0.7)

    if not message:
        return jsonify({"error": "Missing message"}), 400

    # Retrieve the custom prompt from the JSON data if a prompt_id is provided
    prompts = read_data()
    prompt = next((item for item in prompts if item['prompt_id'] == prompt_id), None)
    if prompt:
        message = prompt['content'] + " " + message

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": message}]
        )
        return jsonify(response), 200
    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/custom_prompts', methods=['GET'])
def get_all_prompts():
    prompts = read_data()
    return jsonify(prompts), 200

@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    # Assuming you have session setup
    session.pop('conversation', None)
    return jsonify({'message': 'Conversation reset successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)