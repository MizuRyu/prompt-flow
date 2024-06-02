import os
from promptflow.tracing import start_trace
import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

from dotenv import load_dotenv

load_dotenv()
start_trace(collection="autogen-groupchat")

# log取得開始
# logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})


config_list = [{"model": "gpt-35-turbo-1106", "api_key": os.getenv("AOAI_KEY"), "api_version": os.getenv("AOAI_VERSION"), "base_url": os.getenv("AOAI_BASE"), "api_type": "azure"}]
llm_config = {"config_list": config_list, "timeout": 600}

user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
)

bakery = AssistantAgent(
    name="Bakery",
    system_message="あなたはパン屋さんです。パンに関係することのみ答えます",
    llm_config=llm_config,
)
fish = AssistantAgent(
    name="Fishstore",
    system_message="あなたは魚屋さんです。お魚に関係することのみ答えます。",
    llm_config=llm_config,
)
meat = AssistantAgent(
    name="Meatstore",
    system_message="あなたは肉屋さんです。お肉に関係することのみ答えます。",
    llm_config=llm_config,
)

agents =[user_proxy, bakery, fish, meat]

group_chat = GroupChat(
    agents=agents,
    messages=[],
    max_round=10,
    speaker_transitions_type="allowed"
)

# Create the manager
manager = GroupChatManager(
    groupchat=group_chat, llm_config=llm_config, code_execution_config=False
)
user_proxy.initiate_chat(
    manager, message="おいしいステーキの焼き方とクロワッサンの作り方を一行で簡潔に教えて",
    clear_history=True
)

# log取得終了
# autogen.runtime_logging.stop()