import os
from typing import Optional

import dotenv
from openai import OpenAI

dotenv.load_dotenv()


class OpenAIClient:
    def __init__(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.model_name = model_name or os.getenv("LLM_MODEL_NAME")
        self.client = OpenAI(
            api_key=api_key or os.getenv("LLM_API_KEY"),
            base_url=base_url or os.getenv("LLM_BASE_URL"),
        )

    def get_response(self, messages: list[dict[str, str]]) -> str:
        """Get a response from the LLM (qwen).

        Args:
            messages: A list of message dictionaries.

        Returns:
            The LLM's response as a string.
        """
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    client = OpenAIClient()
    # Testing.
    print(client.get_response([{"role": "user", "content": "你是谁？"}]))
