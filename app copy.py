from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import openai
import os
from dotenv import load_dotenv


app = Flask(__name__)
# Configure server-side session with Flask-Session
app.config['SECRET_KEY'] = 'adgadg467537ghdfstsert'  # Set this to a complex random value



# Load environment variables from .env file
load_dotenv()


# Use a consistent database URI across your application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prompts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
    # Define a model for the prompts
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)  # Changed from db.String(200) to db.Text


    def __repr__(self):
        return f'<Prompt {self.prompt_id}>'

# Create the database file and tables
with app.app_context():
    db.create_all()

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
    
    prompt = Prompt.query.filter_by(prompt_id=prompt_id).first()
    if prompt is None:
        prompt = Prompt(prompt_id=prompt_id, content=content)
        db.session.add(prompt)
    else:
        prompt.content = content
    db.session.commit()
    
    return jsonify({'message': 'Prompt saved successfully', 'prompt_id': prompt.prompt_id}), 201

@app.route('/custom_prompt/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    prompt = Prompt.query.filter_by(prompt_id=prompt_id).first()
    if prompt:
        return jsonify({'prompt_id': prompt.prompt_id, 'content': prompt.content}), 200
    else:
        return jsonify({'error': 'Prompt not found'}), 404

@app.route('/custom_prompt/<prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    
    prompt = Prompt.query.filter_by(prompt_id=prompt_id).first()
    if prompt:
        prompt.content = content
        db.session.commit()
        return jsonify({'message': 'Prompt updated', 'prompt_id': prompt.prompt_id}), 200
    else:
        return jsonify({'error': 'Prompt not found'}), 404

@app.route('/custom_prompt/<prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    prompt = Prompt.query.filter_by(prompt_id=prompt_id).first()
    if prompt:
        db.session.delete(prompt)
        db.session.commit()
        return jsonify({'message': 'Prompt deleted'}), 200
    else:
        return jsonify({'error': 'Prompt not found'}), 404

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    prompt_id = data.get('prompt_id')
    temperature = data.get('temperature', 0.7)

    if not message:
        return jsonify({"error": "Missing message"}), 400

    # Retrieve the custom prompt from the database if a prompt_id is provided
    if prompt_id:
        prompt = Prompt.query.filter_by(prompt_id=prompt_id).first()
        if prompt is None:
            return jsonify({'error': 'Prompt not found'}), 404
        message = prompt.content + " " + message

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            # model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )
        return jsonify(response), 200
    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/custom_prompts', methods=['GET'])
def get_all_prompts():
    prompts = Prompt.query.all()
    return jsonify([{'prompt_id': prompt.prompt_id, 'content': prompt.content} for prompt in prompts]), 200

@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    session.pop('conversation', None)  # This clears the conversation from the session
    return jsonify({'message': 'Conversation reset successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
