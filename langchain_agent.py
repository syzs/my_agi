from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool, tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent

import calendar
from dateutil import parser as dateParser
from langchain import hub
import json

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class ReActAgent:

    @tool("weekday")
    def weekday(date_str: str) -> str:
        """Convert date to weekday name"""
        # January 18, 1979
        print(date_str)
        date_str = date_str.strip().rstrip('"')
        d = dateParser.parse(date_str)

        return calendar.day_name[d.weekday()]

    def run(self):
        search = SerpAPIWrapper()
        tools = [
            Tool.from_function(
                func=search.run,
                name='Search',  # -> 自定义 @tool('weekday')
                description='useful for when you need to answer questions about current events'
                # 自定义  -> """Convert date to weekday name"""
            )
        ]
        tools += [self.weekday]

        # 下载一个现有的prompt
        prompt = hub.pull("hwchase17/react")
        # print(prompt.template)
        '''
        Answer the following questions as best you can. You have access to the following tools:

        {tools}
        
        Use the following format:
        
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        Begin!
        
        Question: {input}
        Thought:{agent_scratchpad}
        '''

        llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)

        # 定义一个 agent: 需要大模型、工具集、和 Prompt 模板
        agent = create_react_agent(llm, tools, prompt)
        # 定义一个执行器：需要 agent 对象 和 工具集
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        agent_executor.invoke({"input": "周杰伦生日那天是周几"})


from langchain.agents import create_self_ask_with_search_agent


class SelfAskWithSearchAgent:
    def run(self):
        # 下载一个模板
        prompt = hub.pull("hwchase17/self-ask-with-search")
        # print(prompt.template)

        search = SerpAPIWrapper()

        tools = [
            Tool(
                name="Intermediate Answer",
                func=search.run,
                description="useful for when you need to ask with search.",
            )
        ]

        llm = ChatOpenAI(model_name='gpt-4', temperature=0)

        # self_ask_with_search_agent 只能传一个名为 'Intermediate Answer' 的 tool
        agent = create_self_ask_with_search_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        agent_executor.invoke({"input": "吴京的老婆主持过哪些综艺节目"})


from langchain.agents.openai_assistant import OpenAIAssistantRunnable


class OpenAIAssistantAgent:
    def run(self):
        interpreter_assistant = OpenAIAssistantRunnable.create_assistant(
            name="langchain assistant",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-3.5-turbo",
        )
        output = interpreter_assistant.invoke({"content": "10减4的差的2.3次方是多少"})

        print(output[0].content[0].text.value)


if __name__ == '__main__':
    agent = OpenAIAssistantAgent()
    agent.run()
