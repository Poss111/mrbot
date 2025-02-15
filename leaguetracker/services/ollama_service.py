import json
from typing import List
import requests
import structlog

from leaguetracker.models.context import Context


class OllamaService:
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        """
        Initializes the Ollama service client.

        :param model_name: The name of the model being used.
        :param base_url: The base URL where Ollama is running.
        """
        self.model_name = model_name
        self.base_url = base_url

    def generate_response(self, prompt: str, system_prompt: str = None, stream: bool = False) -> str:
        """
        Sends a prompt to the Ollama model and retrieves a response.

        :param prompt: The user input text.
        :param system_prompt: Optional system instructions for the model.
        :return: The model's response text.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
        }
        
        structlog.get_logger().info("Sending prompt to Ollama", payload=payload)
        
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()  # Raise an error for HTTP issues

            if stream:
                return self._parse_streaming_response(response)
            else:
                data = response.json()
                return data.get("response", "").strip()
        except requests.RequestException as e:
            return f"Error communicating with Ollama: {str(e)}"
    
    def generate_chat_response(self, context: List[Context], system_prompt: str = None, stream: bool = False) -> str:
        """
        Sends a prompt to the Ollama model and retrieves a response.

        :param prompt: The user input text.
        :param system_prompt: Optional system instructions for the model.
        :return: The model's response text.
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": [context_item.to_dict() for context_item in context],
        }
        
        structlog.get_logger().info("Sending prompt to Ollama", payload=payload)
        
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()  # Raise an error for HTTP issues

            if stream:
                return self._parse_streaming_chat_response(response)
            else:
                data = response.json()
                return data.get("response", "").strip()
        except requests.RequestException as e:
            return f"Error communicating with Ollama: {str(e)}"
        

    def _parse_streaming_response(self, response) -> str:
        """
        Parses a streaming response from Ollama.

        :param response: The response object from requests.
        :return: The combined response text.
        """
        collected_text = []
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    collected_text.append(json_data.get("response", "").strip())
                except json.JSONDecodeError:
                    continue  # Skip malformed lines
        return " ".join(collected_text).strip()
        

    def _parse_streaming_chat_response(self, response) -> str:
        """
        Parses a streaming response from Ollama.

        :param response: The response object from requests.
        :return: The combined response text.
        """
        collected_text = []
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    collected_text.append(json_data.get("message", "").get("content", "").strip())
                except json.JSONDecodeError:
                    continue  # Skip malformed lines
        return " ".join(collected_text).strip()