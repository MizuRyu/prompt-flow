from promptflow.core import tool
from promptflow.connections import AzureOpenAIConnection, CustomConnection

@tool
def my_python_tool(
    redisConnection: CustomConnection,
    question: str,
    azureOpenAiConnection: AzureOpenAIConnection,
    azureOpenAiModelName: str = "gpt-4-32k",
    autogen_workflow_id: int = 1,
) -> str:
    print("Hello Promptflow")