import requests


class Generator:
    """Generate answers using a local Ollama model."""

    def __init__(self, model="qwen2.5:3b", base_url="http://localhost:11434"):
        """
        Initialize the Generator.

        Args:
            model (str): Ollama model name.
            base_url (str): Ollama server URL.
        """
        self.model = model
        self.base_url = base_url

    def generate(self, prompt):
        """
        Generate a response from the language model.

        Args:
            prompt (str): Complete prompt sent to the LLM.

        Returns:
            str: Generated response.
        """

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]
