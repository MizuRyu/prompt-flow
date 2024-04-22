import json
from typing import Any, Dict, List

import autogen

class AgNestedChat:
    def __init__(self, config_list: List[Dict[str, Any]]) -> None:
        
        self.workflows = {}

        self.config_list = config_list

        self.llm_config = {
            "cache_seed": False,
            "temperature": 0,
            "config_list": self.config_list,
            "timeout": 120
        }

        self.writer = autogen.AssistantAgent(
            name="Writer",
            llm_config={"config_list": config_list},
            system_message="""
            あなたは優秀なライターです。旅行業界に精通しており、満足度の高い評価を得るブログ記事を書くことに精通しています。
            あなたは難しい用語やシナリオを伝わる物語に変えることができます。
            ユーザーからのフィードバックに基づき、コンテンツの質を向上させる必要があります。
            """
        )

        self.user_proxy = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            is_termination_msg=lambda x: x.get("context", "").find("TERMINATE") >= 0,
            code_execution_config={
                "last_n_messages": 1,
                "work_dir": "tasks",
                "use_docker": False,
            },
        )

        self.critic = autogen.AssistantAgent(
            name="Critic",
            llm_config = {"config_list": config_list},
            system_message="""
            あなたは批評家であり、成果物の品質に対してこだわりを持っている批評家として有名です。
            あなたの仕事は、コンテンツに有害な要素や規制違反がないか精査し、すべての素材が要求されるガイドラインに合致していることを確認することです。
            すべての素材が必要なガイドラインに合致していることを確認する。
            """
        )

        def reply_callback(agent, messages=[], sender=None, config=None):
            return False, None
        
        agents_list = [self.writer, self.user_proxy, self.critic]
        for agent in agents_list:
            agent.register_reply(
                [autogen.Agent, None],
                reply_func=reply_callback,
                config={"callback": None}
            )

    def _reflection_message(self, recipient, messages, sender, config):
        print("実行中", "yellow")
        return f"以下の文章を振り返り、批評する.\n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"

    def chat(self, question: str) -> autogen.ChatResult:
        # UserProxyの登録
        self.user_proxy.register_nested_chats(
            [
                {
                    "recipient": self.critic,
                    "message": self._reflection_message,
                    "summary_method": "last_msg",
                    "max_turns": 1
                }
            ],
            trigger=self.writer
        )

        res = self.user_proxy.initiate_chat(
            recipient=self.writer,
            message=question,
            max_turns=2,
            summary_method="last_msg"
        )
        return res