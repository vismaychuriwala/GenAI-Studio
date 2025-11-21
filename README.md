# GenAI Studio

A modular, extensible chatbot application built with LangChain and Streamlit.

## Features

- 🤖 **Configurable AI Agents** - Easy-to-extend agent architecture
- 📝 **Editable System Prompts** - Customize agent behavior via text files
- ⚙️ **YAML Configuration** - Centralized settings management
- 🔧 **Tool System** - Extensible tools directory for future capabilities
- 💬 **Clean UI** - Built with Streamlit for a modern chat interface

## Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
GenAI-Studio/
├── agents/              # Agent implementations
│   ├── __init__.py
│   └── basic_agent.py   # Basic conversational agent
├── tools/               # Tool implementations (extensible)
│   └── __init__.py
├── prompts/             # System prompts for agents
│   └── basic_agent.txt  # Prompt for basic agent
├── config.yaml          # Application configuration
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── .gitignore          # Git ignore rules
```

## Configuration

Edit `config.yaml` to customize:

- **App Settings**: Title, icon, page title
- **Agent Settings**: Which agent to use, model name, temperature
- **System Prompts**: Reference different prompt files

Example:

```yaml
app:
  title: "GenAI Studio Assistant"
  icon: "🤖"

agent:
  type: "basic_agent"
  model: "gpt-3.5-turbo"
  temperature: 0.7
  system_prompt_file: "basic_agent.txt"
```

## Customization

### Changing the System Prompt

Edit `prompts/basic_agent.txt` to change how the agent behaves.

### Switching Models

In `config.yaml`, change the `agent.model` field:
- `gpt-3.5-turbo` (faster, cheaper)
- `gpt-4` (more capable)
- `gpt-4-turbo-preview` (balance)

### Adjusting Temperature

Set `agent.temperature` (0.0 - 2.0):
- Lower (0.0-0.3): More focused and deterministic
- Medium (0.5-0.8): Balanced
- Higher (0.9-2.0): More creative and varied

## Extending the Project

See [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for detailed information on:
- Creating new agents
- Adding tools
- Architecture patterns
- Best practices

See [STYLE_GUIDE.md](STYLE_GUIDE.md) for:
- Coding conventions
- File organization
- Documentation standards

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in `requirements.txt`

## Contributing

1. Follow the style guide in [STYLE_GUIDE.md](STYLE_GUIDE.md)
2. Test your changes thoroughly
3. Update documentation as needed
4. Keep the modular architecture intact

## License

This project is open source and available for modification and extension.
