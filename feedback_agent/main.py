import os

import autogen
from dotenv import load_dotenv

load_dotenv()

# env set
config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json"
)
llm_config = {"config_list": config_list}

assinstant = autogen.AssistantAgent(name="assistant", llm_config=llm_config)

goal_task = "FastAPIに関する簡潔で魅力的なブログ記事を書く"

print(assinstant)

# ワークフロー
# 登場人物: 3人のエージェント user_proxy | ライター | 批評家

# system_prompt
writer_system_prompt = """
あなたは優秀なライターです。旅行業界に精通しており、満足度の高い評価を得るブログ記事を書くことに精通しています。
あなたは難しい用語やシナリオを伝わる物語に変えることができます。
ユーザーからのフィードバックに基づき、コンテンツの質を向上させる必要があります。
"""

critic_system_prompt = """
あなたは批評家であり、成果物の品質に対してこだわりを持っている批評家として有名です。
あなたの仕事は、コンテンツに有害な要素や規制違反がないか精査し、すべての素材が要求されるガイドラインに合致していることを確認することです。
すべての素材が必要なガイドラインに合致していることを確認する。
"""

### エージェントの定義 ###
# ライター
writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message=writer_system_prompt
)

# user proxy
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    }
)

# 批評家
critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message=critic_system_prompt
)


### タスクの実行 ###
def reflection_message(recipient, messages, sender, config):
    print("実行中...", "yellow")
    return f"ライターによる記事を批評する. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"

user_proxy.register_nested_chats(
    [{"recipient": critic, "message": reflection_message, "summary_method": "last_msg", "max_turns": 1}],
    trigger=writer,  # condition=my_condition,
)

res = user_proxy.initiate_chat(recipient=writer, message=goal_task, max_turns=2, summary_method="last_msg")

# Issue: 批判を受けてから文章を再構築するように命令を足す必要がある？？
# 