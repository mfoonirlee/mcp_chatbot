import asyncio
import os
from typing import Any

from mcp_chatbot import ChatSession, Configuration, Server
from mcp_chatbot.llm.oai import OpenAIClient as LLMClient


def parse_servers_config(config: dict[str, Any]) -> list[Server]:
    return [
        Server(name, srv_config) for name, srv_config in config["mcpServers"].items()
    ]


async def main() -> None:
    """Initialize and run the chat session."""
    config = Configuration()
    # You can change the config file to the one you want to use
    server_config = config.load_config("mcp_servers/servers_config.json")
    servers = parse_servers_config(server_config)
    llm_client = LLMClient(
        model_name=config.llm_model_name,
        api_key=config.llm_api_key,
        base_url=config.llm_base_url,
    )
    chat_session = ChatSession(servers, llm_client)

    markdown_folder_path = os.getenv("MARKDOWN_FOLDER_PATH")
    result_folder_path = os.getenv("RESULT_FOLDER_PATH")

    if "/path/to/your" in markdown_folder_path or "/path/to/your" in result_folder_path:
        raise ValueError(
            "markdown_folder_path or result_folder_path can not contain /path/to/folder"
            "Please set the correct path in the .env file"
        )

    try:
        await chat_session.initialize()
        await chat_session.run(
            f"Please summarize the content of the {markdown_folder_path} folder "
            "in one sentence. (use Chinese)"
        )
    finally:
        await chat_session.cleanup_servers()


if __name__ == "__main__":
    asyncio.run(main())
