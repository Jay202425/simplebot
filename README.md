# Mistral AI Bot

A conversational AI bot powered by Mistral AI, with both CLI and Streamlit interfaces.

## Features

- **Interactive Chat**: Real-time conversation with Mistral AI
- **Multiple Interfaces**: Command-line and Streamlit web interface
- **Easy to Use**: Simple and intuitive interaction

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mistral-ai-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/Scripts/Activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set your Mistral API key in the code or as an environment variable:
```python
api_key = "your_api_key_here"
```

## Usage

### CLI Version
Run the command-line bot:
```bash
python bot.py
```

### Streamlit Version
Run the web interface:
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## API Key

Get your Mistral AI API key from [console.mistral.ai](https://console.mistral.ai)

## License

MIT License

## Author

Created with Mistral AI
