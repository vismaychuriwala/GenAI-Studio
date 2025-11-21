# Style Guide

This document defines coding standards and conventions for the GenAI Studio project.

## Table of Contents

- [Python Style](#python-style)
- [File Organization](#file-organization)
- [Naming Conventions](#naming-conventions)
- [Documentation](#documentation)
- [Configuration](#configuration)
- [Git Conventions](#git-conventions)

---

## Python Style

### General Guidelines

Follow [PEP 8](https://pep8.org/) with the following specifics:

- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Maximum 100 characters
- **Encoding**: UTF-8
- **Quotes**: Use double quotes for strings by default

### Imports

Order imports in three groups separated by blank lines:

```python
# 1. Standard library imports
import os
import sys
from typing import Optional, List

# 2. Third-party imports
import streamlit as st
import yaml
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 3. Local application imports
from agents import BasicAgent
from tools import SearchTool
```

### Type Hints

Always use type hints for function parameters and return values:

```python
def chat(self, user_message: str) -> str:
    """Process user message and return response."""
    pass

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    pass

def initialize_agent(api_key: str, model: str = "gpt-3.5-turbo",
                     temperature: float = 0.7) -> BasicAgent:
    """Initialize and return configured agent."""
    pass
```

### Class Structure

Order class members consistently:

```python
class MyAgent:
    # 1. Class variables
    DEFAULT_MODEL = "gpt-3.5-turbo"

    # 2. __init__ method
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.api_key = api_key
        self.model = model

    # 3. Public methods
    def chat(self, message: str) -> str:
        pass

    def clear_history(self):
        pass

    # 4. Private methods (prefixed with _)
    def _load_prompt(self, path: str) -> str:
        pass

    def _build_messages(self) -> list:
        pass
```

### Error Handling

Use specific exceptions and always provide context:

```python
# Good
try:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Configuration file not found: {config_path}")
except yaml.YAMLError as e:
    raise ValueError(f"Invalid YAML in {config_path}: {e}")

# Bad
try:
    config = yaml.safe_load(open(config_path))
except Exception as e:
    print(f"Error: {e}")
```

### Function Length

- Keep functions focused on a single task
- Aim for functions under 50 lines
- Extract complex logic into helper functions

```python
# Good - focused function
def load_system_prompt(prompt_path: str) -> str:
    """Load system prompt from file."""
    if not os.path.exists(prompt_path):
        return self._get_default_prompt()

    with open(prompt_path, 'r') as f:
        return f.read().strip()

# Better - extracted helper
def _get_default_prompt(self) -> str:
    """Return default system prompt."""
    return "You are a helpful AI assistant."
```

---

## File Organization

### Directory Structure

```
GenAI-Studio/
├── agents/              # Agent implementations
│   ├── __init__.py     # Export all agents
│   ├── base_agent.py   # Base agent class (optional)
│   └── basic_agent.py  # Specific agent implementation
├── tools/              # Tool implementations
│   ├── __init__.py
│   └── search_tool.py
├── prompts/            # System prompts (text files)
│   ├── basic_agent.txt
│   └── rag_agent.txt
├── utils/              # Utility functions (future)
│   └── __init__.py
├── tests/              # Test files (future)
│   └── test_agents.py
├── docs/               # Additional documentation (future)
├── config.yaml         # Main configuration
├── app.py              # Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .gitignore
├── README.md
├── PROJECT_GUIDE.md
└── STYLE_GUIDE.md
```

### File Naming

- **Python files**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase`
- **Config files**: `lowercase.yaml` or `lowercase.json`
- **Prompt files**: `agent_name.txt`
- **Documentation**: `UPPERCASE.md` for top-level docs

### Module Organization

Each agent/tool should be in its own file:

```
agents/
├── __init__.py          # from .basic_agent import BasicAgent
├── basic_agent.py       # class BasicAgent
├── rag_agent.py         # class RAGAgent
└── function_agent.py    # class FunctionAgent
```

---

## Naming Conventions

### Variables and Functions

```python
# Variables: lowercase_with_underscores
api_key = os.getenv("OPENAI_API_KEY")
system_prompt_path = "prompts/basic.txt"
conversation_history = []

# Functions: lowercase_with_underscores
def load_config(path: str) -> dict:
    pass

def initialize_agent(api_key: str) -> BasicAgent:
    pass

# Private functions: prefix with underscore
def _load_prompt_from_file(path: str) -> str:
    pass
```

### Classes

```python
# Classes: PascalCase
class BasicAgent:
    pass

class RAGAgent:
    pass

class SearchTool:
    pass
```

### Constants

```python
# Constants: UPPER_CASE_WITH_UNDERSCORES
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
MAX_HISTORY_LENGTH = 100
PROMPTS_DIRECTORY = "prompts"
```

### Configuration Keys

Use lowercase with underscores in YAML:

```yaml
# Good
app:
  page_title: "GenAI Studio"
  default_model: "gpt-3.5-turbo"

agent:
  system_prompt_file: "basic_agent.txt"

# Avoid
app:
  pageTitle: "GenAI Studio"
  PageTitle: "GenAI Studio"
```

---

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def chat(self, user_message: str, context: Optional[dict] = None) -> str:
    """Process user message and generate response.

    Args:
        user_message: The message from the user
        context: Optional context dictionary with additional information

    Returns:
        The agent's response as a string

    Raises:
        ValueError: If user_message is empty
        APIError: If the LLM API call fails

    Example:
        >>> agent = BasicAgent(api_key="...")
        >>> response = agent.chat("Hello!")
        >>> print(response)
        "Hello! How can I help you today?"
    """
    if not user_message:
        raise ValueError("User message cannot be empty")

    # Implementation...
```

### Class Docstrings

```python
class BasicAgent:
    """A basic conversational agent using LangChain and OpenAI.

    This agent maintains conversation history and uses a system prompt
    loaded from a file to guide its behavior.

    Attributes:
        llm: The ChatOpenAI instance used for generation
        conversation_history: List of past messages
        system_message: The system prompt message

    Example:
        >>> agent = BasicAgent(
        ...     api_key="sk-...",
        ...     model="gpt-3.5-turbo",
        ...     system_prompt_path="prompts/basic_agent.txt"
        ... )
        >>> response = agent.chat("What is Python?")
    """
```

### Inline Comments

Use comments sparingly and only for complex logic:

```python
# Good - explains WHY, not WHAT
# Limit history to last 10 messages to manage token usage
if len(self.conversation_history) > 10:
    self.conversation_history = self.conversation_history[-10:]

# Bad - obvious from the code
# Set the temperature to 0.7
temperature = 0.7
```

### README and Guides

- **README.md**: Quick start, basic usage, project overview
- **PROJECT_GUIDE.md**: Detailed architecture, extension guides
- **STYLE_GUIDE.md**: Coding standards (this document)
- Keep examples up-to-date with current code
- Use code blocks with language specification

---

## Configuration

### YAML Formatting

```yaml
# Use 2-space indentation
# Add comments for clarity
# Group related settings

# Application configuration
app:
  title: "GenAI Studio Assistant"
  icon: "🤖"
  page_title: "GenAI Studio"

# Agent configuration
agent:
  type: "basic_agent"  # Options: basic_agent, rag_agent
  model: "gpt-3.5-turbo"  # OpenAI model name
  temperature: 0.7  # Range: 0.0 to 2.0
  system_prompt_file: "basic_agent.txt"  # File in prompts/

# API configuration
api:
  provider: "openai"  # Future: anthropic, cohere, etc.
  timeout: 30  # Seconds
```

### Environment Variables

```bash
# .env file format
# Use UPPER_CASE for environment variables
# Group by service/purpose

# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...  # Optional

# Application Settings
DEBUG=false
LOG_LEVEL=INFO

# Future services
# PINECONE_API_KEY=...
# ANTHROPIC_API_KEY=...
```

### Configuration Loading

```python
# Load configuration early in the application
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load YAML config
def load_config(config_path: str = "config.yaml") -> dict:
    """Load and validate configuration."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")

    # Validate required keys
    required_keys = ["app", "agent"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    return config
```

---

## Git Conventions

### Commit Messages

Follow the Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(agent): add RAG agent with vector search

Implemented a new RAGAgent class that supports:
- Document embedding and storage
- Similarity search
- Context-aware responses

Closes #123

---

fix(config): handle missing prompt file gracefully

Previously would crash if prompt file didn't exist.
Now falls back to default prompt with warning.

---

docs: update PROJECT_GUIDE with tool creation examples

Added comprehensive examples for creating custom tools
and integrating them with agents.
```

### Branch Naming

```
<type>/<short-description>

Examples:
feature/rag-agent
fix/config-loading-error
docs/update-readme
refactor/agent-base-class
```

### .gitignore

Keep `.gitignore` updated:

```gitignore
# Virtual environment
venv/
env/
.env

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Logs
*.log

# Data (if applicable)
data/
*.db
*.sqlite
```

---

## Testing (Future)

### Test File Organization

```
tests/
├── __init__.py
├── test_agents.py
├── test_tools.py
└── test_config.py
```

### Test Naming

```python
# Test functions: test_<what>_<condition>_<expected>
def test_agent_initialization_with_valid_key_succeeds():
    pass

def test_agent_chat_with_empty_message_raises_error():
    pass

def test_config_loading_with_invalid_yaml_raises_error():
    pass
```

### Test Structure

```python
def test_agent_chat_returns_response():
    # Arrange
    agent = BasicAgent(api_key="test-key", model="gpt-3.5-turbo")
    user_message = "Hello"

    # Act
    response = agent.chat(user_message)

    # Assert
    assert isinstance(response, str)
    assert len(response) > 0
```

---

## Code Review Checklist

Before submitting code for review:

- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have type hints
- [ ] All classes and functions have docstrings
- [ ] No hardcoded secrets or API keys
- [ ] Configuration changes documented
- [ ] README updated if needed
- [ ] No unnecessary print statements
- [ ] Error handling is appropriate
- [ ] Variable names are descriptive
- [ ] No unused imports or variables
- [ ] Code is tested manually
- [ ] Commit messages follow conventions

---

## Tools and Linters

### Recommended Tools

```bash
# Install development tools
pip install black flake8 mypy pylint

# Format code
black .

# Check style
flake8 .

# Type checking
mypy agents/ tools/

# Linting
pylint agents/ tools/
```

### Configuration Files

**pyproject.toml** (for Black):
```toml
[tool.black]
line-length = 100
target-version = ['py38']
```

**.flake8**:
```ini
[flake8]
max-line-length = 100
exclude = venv/,__pycache__/
```

---

## Best Practices Summary

1. **Consistency**: Follow established patterns in the codebase
2. **Simplicity**: Write simple, readable code over clever code
3. **Documentation**: Document WHY, not WHAT
4. **Type Safety**: Use type hints everywhere
5. **Error Handling**: Be specific with exceptions
6. **Configuration**: Use config files, not hardcoded values
7. **Modularity**: Keep components loosely coupled
8. **Testing**: Test at multiple levels (future)
9. **Version Control**: Commit often, write clear messages
10. **Review**: Review your own code before pushing

---

## Questions or Suggestions?

If you have questions about these guidelines or suggestions for improvements:

1. Open an issue on the project repository
2. Discuss in team meetings
3. Propose changes via pull request

Remember: These are guidelines, not rules. Use good judgment!
