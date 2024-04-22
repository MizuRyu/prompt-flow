from promptflow.core import tool
from promptflow.connections import AzureOpenAIConnection, CustomConnection
from agentchat_nestedchat import AgNestedChat

import os
from dotenv import load_dotenv

load_dotenv()

@tool
def my_python_tool(
    question: str,
    azureOpenAiConnection: AzureOpenAIConnection,
    azureOpenAiModelName: str = "gpt-3.5-turbo-1106",
    autogen_workflow_id: int = 1,
) -> str:
    aoai_api_base = azureOpenAiConnection.api_base
    aoai_api_key = azureOpenAiConnection.api_key
    aoai_api_version = azureOpenAiConnection.api_version
    # aoai_api_base = os.getenv("AOAI_BASE")
    # aoai_api_key = os.getenv("AOAI_KEY")
    # aoai_api_version = os.getenv("AOAI_VERSION")
    OAI_CONFIG_LIST = [
        {
            "model": azureOpenAiModelName,
            "api_key": aoai_api_key,
            "base_url": aoai_api_base,
            "api_type": "azure",
            "api_version": aoai_api_version
        }
    ]

    if autogen_workflow_id == 1:
        ag_workflow = AgNestedChat(config_list=OAI_CONFIG_LIST)
        res = ag_workflow.chat(question=question)
        return res.summary