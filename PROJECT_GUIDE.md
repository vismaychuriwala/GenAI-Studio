# Project Guide

This guide explains the architecture of GenAI Studio and how to extend it with new agents and tools.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [How Components Work Together](#how-components-work-together)
- [Creating New Agents](#creating-new-agents)
- [Adding Tools](#adding-tools)
- [Configuration System](#configuration-system)
- [Best Practices](#best-practices)

---

## Architecture Overview

GenAI Studio follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────┐
│           app.py (Streamlit UI)             │
│  - Loads config.yaml                        │
│  - Manages session state                    │
│  - Renders chat interface                   │
└──────────────────┬──────────────────────────┘
                   │
                   ├─────> config.yaml
                   │       (Configuration)
                   │
                   ▼
┌─────────────────────────────────────────────┐
│          agents/ (Agent Layer)              │
│  - BasicAgent: Conversational agent         │
│  - Future agents: RAG, function calling...  │
└──────────────────┬──────────────────────────┘
                   │
                   ├─────> prompts/
                   │       (System prompts)
                   │
                   ▼
┌─────────────────────────────────────────────┐
│          tools/ (Tool Layer)                │
│  - Custom tools for agent capabilities      │
│  - Search, calculator, API calls, etc.      │
└─────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│       LangChain/OpenAI (LLM Layer)          │
└─────────────────────────────────────────────┘
```

---

## How Components Work Together

### 1. Application Startup (app.py)

When you run `streamlit run app.py`:

1. **Config Loading**: Reads `config.yaml` to get all settings
2. **API Key Loading**: Retrieves OpenAI API key from `.env` file
3. **Agent Initialization**: Creates the agent specified in config
4. **UI Setup**: Configures Streamlit page with title and icon

```python
# From app.py
config = yaml.safe_load(open("config.yaml"))
agent = BasicAgent(
    api_key=api_key,
    model=config["agent"]["model"],
    temperature=config["agent"]["temperature"],
    system_prompt_path="prompts/basic_agent.txt",
    reasoning_effort=config["agent"].get("reasoning_effort")
)
```

### 2. Agent Initialization (agents/basic_agent.py)

The agent initializes with:

1. **LLM Setup**: Creates ChatOpenAI instance with specified model
2. **Prompt Loading**: Reads system prompt from file
3. **History Management**: Initializes empty conversation history

```python
# Simplified agent initialization
llm_params = {"model": model, "temperature": temperature}
if reasoning_effort:
    llm_params["reasoning_effort"] = reasoning_effort
self.llm = ChatOpenAI(**llm_params)
self.system_message = SystemMessage(content=prompt_from_file)
self.conversation_history = []
```

### 3. Chat Flow

When a user sends a message:

```
User Input → Streamlit UI → Agent.chat()
                                │
                                ├─ Add to history
                                ├─ Build messages (system + history)
                                ├─ Call LLM
                                ├─ Store response
                                └─ Return response
                                    │
Response ← Streamlit UI ←──────────┘
```

---

## Creating New Agents

### Step 1: Create Agent File

Create a new file in `agents/` directory, e.g., `agents/rag_agent.py`:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os


class RAGAgent:
    def __init__(self, api_key: str, model: str = "gpt-5-mini",
                 temperature: float = 1.0, system_prompt_path: str = None,
                 reasoning_effort: str = None):
        llm_params = {
            "api_key": api_key,
            "model": model,
            "temperature": temperature
        }
        if reasoning_effort:
            llm_params["reasoning_effort"] = reasoning_effort

        self.llm = ChatOpenAI(**llm_params)
        self.conversation_history = []

        # Load system prompt
        if system_prompt_path and os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r') as f:
                system_prompt = f.read().strip()
        else:
            system_prompt = "You are a helpful AI assistant with access to documents."

        self.system_message = SystemMessage(content=system_prompt)

        # Add your RAG initialization here
        # self.vector_store = ...
        # self.retriever = ...

    def chat(self, user_message: str) -> str:
        # Add RAG logic here
        # 1. Retrieve relevant documents
        # 2. Build context
        # 3. Query LLM with context

        self.conversation_history.append(HumanMessage(content=user_message))
        messages = [self.system_message] + self.conversation_history
        response = self.llm.invoke(messages)
        self.conversation_history.append(AIMessage(content=response.content))
        return response.content

    def clear_history(self):
        self.conversation_history = []
```

### Step 2: Update agents/__init__.py

```python
from .basic_agent import BasicAgent
from .rag_agent import RAGAgent

__all__ = ['BasicAgent', 'RAGAgent']
```

### Step 3: Create System Prompt

Create `prompts/rag_agent.txt`:

```
You are a RAG-powered AI assistant with access to a knowledge base.

Your capabilities:
- Answer questions using retrieved documents
- Cite sources when providing information
- Admit when information is not in the knowledge base

Always be accurate and cite your sources.
```

### Step 4: Update config.yaml

```yaml
agent:
  type: "rag_agent"  # Change this
  model: "gpt-5-mini"
  temperature: 1.0
  reasoning_effort: "minimal"
  system_prompt_file: "rag_agent.txt"  # Change this
```

### Step 5: Update app.py (if needed)

If your agent has different initialization parameters, update the agent creation logic in `app.py`:

```python
# Add dynamic agent loading
agent_type = config["agent"]["type"]

if agent_type == "basic_agent":
    from agents import BasicAgent
    agent = BasicAgent(...)
elif agent_type == "rag_agent":
    from agents import RAGAgent
    agent = RAGAgent(...)
```

---

## Adding Tools

Tools extend agent capabilities (search, calculation, API calls, etc.).

### Step 1: Create Tool File

Create `tools/search_tool.py`:

```python
from langchain.tools import BaseTool
from typing import Optional


class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Search the web for information"

    def _run(self, query: str) -> str:
        """Execute the search"""
        # Implement your search logic
        # Could use Google API, DuckDuckGo, etc.
        results = self._perform_search(query)
        return results

    async def _arun(self, query: str) -> str:
        """Async version"""
        return self._run(query)

    def _perform_search(self, query: str) -> str:
        # Your search implementation
        pass
```

### Step 2: Update tools/__init__.py

```python
from .search_tool import SearchTool

__all__ = ['SearchTool']
```

### Step 3: Integrate Tool with Agent

Update your agent to use tools:

```python
from langchain.agents import initialize_agent, AgentType
from tools import SearchTool


class ToolAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", ...):
        self.llm = ChatOpenAI(api_key=api_key, model=model)

        # Initialize tools
        tools = [SearchTool()]

        # Create agent with tools
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

    def chat(self, user_message: str) -> str:
        response = self.agent.run(user_message)
        return response
```

### Step 4: Update Configuration

Add tool configuration to `config.yaml`:

```yaml
tools:
  enabled: true
  available:
    - search
    - calculator
```

---

## Configuration System

### config.yaml Structure

```yaml
# Application settings
app:
  title: "Your App Name"
  icon: "🤖"
  page_title: "Page Title"

# Agent configuration
agent:
  type: "basic_agent"           # Which agent to use
  model: "gpt-5-mini"           # OpenAI model (gpt-5, gpt-5-mini, gpt-5-nano)
  temperature: 1.0              # Response randomness (1.0 for GPT-5)
  reasoning_effort: "minimal"   # GPT-5 reasoning: minimal, low, medium, high
  system_prompt_file: "basic_agent.txt"  # Prompt file

# API settings
api:
  provider: "openai"            # Future: support other providers

# Tool settings (optional)
tools:
  enabled: false
  available: []
```

### Loading Configuration in Code

```python
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Access config values
title = config["app"]["title"]
model = config["agent"]["model"]
```

---

## Best Practices

### Agent Development

1. **Consistent Interface**: All agents should have:
   - `__init__()` with standard parameters
   - `chat(user_message: str) -> str` method
   - `clear_history()` method

2. **System Prompts**: Always support loading from files
   - Makes prompts easy to edit
   - No code changes needed for prompt updates

3. **Error Handling**: Handle API failures gracefully
   ```python
   try:
       response = self.llm.invoke(messages)
   except Exception as e:
       return f"Error: {str(e)}"
   ```

4. **State Management**: Keep agents stateless or use Streamlit session state
   - Don't rely on global variables
   - Use `st.session_state` for persistence

### Tool Development

1. **Single Responsibility**: Each tool should do one thing well
2. **Clear Descriptions**: Help LLM understand when to use the tool
3. **Type Hints**: Use type hints for better IDE support
4. **Documentation**: Add docstrings explaining tool behavior

### Configuration

1. **Environment Variables**: Use `.env` for secrets (API keys)
2. **YAML for Settings**: Use `config.yaml` for non-secret configuration
3. **Defaults**: Always provide sensible defaults
4. **Validation**: Validate config on startup

### Testing

1. **Test Agents Independently**: Test without UI first
   ```python
   agent = BasicAgent(
       api_key="test",
       model="gpt-5-mini",
       reasoning_effort="minimal"
   )
   response = agent.chat("Hello")
   print(response)
   ```

2. **Mock API Calls**: Use mocking for tests to avoid API costs
3. **Test Configuration**: Test with different config values

---

## Example: Adding a New Agent with Tools

Complete example of adding a "Code Assistant" agent:

### 1. Create `agents/code_agent.py`

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import initialize_agent, AgentType
from tools import PythonREPLTool
import os


class CodeAgent:
    def __init__(self, api_key: str, model: str = "gpt-5",
                 temperature: float = 1.0, system_prompt_path: str = None,
                 reasoning_effort: str = "medium"):
        llm_params = {
            "api_key": api_key,
            "model": model,
            "temperature": temperature
        }
        if reasoning_effort:
            llm_params["reasoning_effort"] = reasoning_effort

        self.llm = ChatOpenAI(**llm_params)

        if system_prompt_path and os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r') as f:
                system_prompt = f.read().strip()
        else:
            system_prompt = "You are a coding assistant."

        tools = [PythonREPLTool()]

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            agent_kwargs={"system_message": system_prompt}
        )

    def chat(self, user_message: str) -> str:
        response = self.agent.run(user_message)
        return response

    def clear_history(self):
        self.agent.memory.clear()
```

### 2. Create `prompts/code_agent.txt`

```
You are an expert coding assistant. Help with code, debugging, and best practices.
```

### 3. Update `config.yaml`

```yaml
agent:
  type: "code_agent"
  model: "gpt-5"
  temperature: 1.0
  reasoning_effort: "medium"
  system_prompt_file: "code_agent.txt"
```

### 4. Update imports in app.py

```python
# Dynamic agent loading
agent_map = {
    "basic_agent": BasicAgent,
    "code_agent": CodeAgent,
}

AgentClass = agent_map.get(config["agent"]["type"], BasicAgent)
agent = AgentClass(...)
```

---

## Troubleshooting

### Agent Not Loading

- Check `config.yaml` syntax (valid YAML)
- Verify agent type matches class name pattern
- Check import in `agents/__init__.py`

### Prompt Not Loading

- Verify file exists in `prompts/` directory
- Check filename matches `system_prompt_file` in config
- Ensure file has `.txt` extension

### API Errors

- Check `.env` file has correct API key
- Verify API key has sufficient credits
- Check model name is valid (OpenAI model list)

---

## Next Steps

- Add document processing for RAG capabilities
- Implement tool calling with function agents
- Add conversation memory persistence
- Create multi-agent workflows
- Add authentication and user management

For coding standards and conventions, see [STYLE_GUIDE.md](STYLE_GUIDE.md).
