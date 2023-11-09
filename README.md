
# Chatbot with Custom Prompts

This project is a Flask-based chatbot that uses OpenAI's GPT models to answer queries based on custom prompts. The application allows users to select a specialization context for the chatbot and interact with it through a web interface.

## Setup Instructions

Follow these steps to get the chatbot up and running on your local machine.

### Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual environment (optional but recommended)

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/sagerock/Nov2023Chatbot
cd your-repository-name
```

2. (Optional) Create and activate a virtual environment:

```bash
# On macOS and Linux:
python3 -m venv env
source env/bin/activate

# On Windows:
python -m venv env
.\env\Scripts\activate
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key. This step varies depending on your operating system.

### Configuration

The chatbot uses a `data.json` file to store custom prompts. You can modify this file to include your own prompts.

#### Modifying `data.json`

The `data.json` file is structured as an array of prompt objects, where each prompt object has a `prompt_id` and `content` field. Here's an example of how the file looks:

```json
[
  {
    "prompt_id": "general",
    "content": "Your general knowledge prompt goes here."
  },
  {
    "prompt_id": "therapy",
    "content": "Your therapy prompt goes here."
  }
  // Add more prompts as needed
]
```

To add a new prompt, simply append a new object to the array with a unique `prompt_id` and the prompt content you wish to use.

Then add your new `prompt_id` to the 'specialization-container' in index.html

### Running the Application

To start the Flask server, run the following command:

```bash
flask run
```

By default, the server will start on `http://127.0.0.1:5000`. Open this address in your web browser to interact with the chatbot.

### Customizing the Front End

The front-end code is contained within the `templates` and `static` directories. You can modify the HTML, CSS, and JavaScript files in these directories to change the appearance and functionality of the web interface.

## Usage

Once the application is running, select a specialization from the dropdown menu and type your message into the chat input. Click the "Send" button to receive a response from the chatbot.

## Contributions

If you wish to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License

