from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os


class BasicAgent:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7,
                 system_prompt_path: str = None, reasoning_effort: str = None):
        llm_params = {
            "api_key": api_key,
            "model": model,
            "temperature": temperature
        }

        if reasoning_effort:
            llm_params["reasoning_effort"] = reasoning_effort

        self.llm = ChatOpenAI(**llm_params)
        self.conversation_history = []

        # Load system prompt from file or use default
        if system_prompt_path and os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r') as f:
                system_prompt = f.read().strip()
        else:
            system_prompt = "You are a helpful AI assistant. Answer questions clearly and concisely."

        self.system_message = SystemMessage(content=system_prompt)

    def chat(self, user_message: str) -> str:
        self.conversation_history.append(HumanMessage(content=user_message))

        messages = [self.system_message] + self.conversation_history

        response = self.llm.invoke(messages)

        self.conversation_history.append(AIMessage(content=response.content))

        return response.content

    def clear_history(self):
        self.conversation_history = []
