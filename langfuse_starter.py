from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

from langfuse import Langfuse
from langfuse.openai import openai


def hello():
    trace = Langfuse().trace(
        name="hello-world",
        user_id="syz",
        release="v0.0.1"
    )

    completion = openai.chat.completions.create(
        name="hello-world",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "对我说'Hello, World!'"}
        ],
        temperature=0,
        trace_id=trace.id,
    )

    print(completion.choices[0].message.content)


from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langfuse.callback import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate


def langchainCallback():
    callhackHandler = CallbackHandler(
        trace_name="SayHello",
        user_id="syz-0",
    )

    model = ChatOpenAI(model="gpt-3.5-turbo-0613")

    prompt = ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template("Say hello to {input}!")
    ])

    # 定义输出解析器
    parser = StrOutputParser()

    chain = (
            {"input": RunnablePassthrough()}
            | prompt
            | model
            | parser
    )

    response = chain.invoke(input="syz-0", config={"callbacks": [callhackHandler]})
    print(response)


from langchain.prompts import PromptTemplate
import uuid
from langfuse.client import Langfuse


class AGIAssistant:
    def __init__(self):
        self.need_answer = PromptTemplate.from_template("""
        *********
        你是AIGC课程的助教，你的工作是从学员的课堂交流中选择出需要老师回答的问题，加以整理以交给老师回答。

        课程内容:
        {outlines}
        *********
        学员输入:
        {user_input}
        *********
        如果这是一个需要老师答疑的问题，回复Y，否则回复N。
        只回复Y或N，不要回复其他内容。""")

        self.check_duplicated = PromptTemplate.from_template("""
        *********
        已有提问列表:
        [
        {question_list}
        ]
        *********
        新提问:
        {user_input}
        *********
        已有提问列表是否有和新提问类似的问题? 回复Y或N, Y表示有，N表示没有。
        只回复Y或N，不要回复其他内容。""")

        self.outlines = """
        LangChain
        模型 I/O 封装
        模型的封装
        模型的输入输出
        PromptTemplate
        OutputParser
        数据连接封装
        文档加载器：Document Loaders
        文档处理器
        内置RAG：RetrievalQA
        记忆封装：Memory
        链架构：Chain/LCEL
        大模型时代的软件架构：Agent
        ReAct
        SelfAskWithSearch
        Assistants API
        LangServe
        LangChain.js
        """

        self.question_list = [
            "谢谢老师",
            "LangChain开源吗",
        ]

        self.model = ChatOpenAI(temperature=0, model_kwargs={"seed": 42})
        self.parser = StrOutputParser()

        self.chain1 = (
                self.need_answer
                | self.model
                | self.parser
        )

        self.chain2 = (
                self.check_duplicated
                | self.model
                | self.parser
        )

    def create_trace(self, user_id):
        langfuse = Langfuse()
        trace_id = str(uuid.uuid4())
        trace = langfuse.trace(
            name='agi-assistant',
            id=trace_id,
            user_id=user_id,
        )
        return trace

    def verify_question(self, question: str, question_list: list, user_id: str) -> bool:
        trace = self.create_trace(user_id)
        callbackHandler = trace.get_langchain_handler()
        # 判断是否需要回答
        chain1Res = self.chain1.invoke({
            'outlines': self.outlines,
            'user_input': question,
        }, config={'callbacks': [callbackHandler]})
        if chain1Res == 'Y':
            # 需要回答的问题，判断是否为重复问题
            chain2Res = self.chain2.invoke({
                'question_list': question_list,
                'user_input': question,
            }, config={'callbacks': [callbackHandler]})
            if chain2Res == 'N':
                question_list.append(question)
                return True
        return False


from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)


class SessionDialogue:
    def __init__(self):
        self.llm = ChatOpenAI()
        self.messages = [
            SystemMessage(content='你是AGIClass的课程助理')
        ]
        self.callbackHandler = CallbackHandler(
            user_id='syz',
            trace_name='session_dialogue',
            session_id=str(uuid.uuid4())
        )

    def run(self):
        while True:
            user_input = input("User:").strip()
            if user_input == "":
                break
            self.messages.append(HumanMessage(content=user_input))
            response = self.llm.invoke(self.messages, config={'callbacks': [self.callbackHandler]})
            print("AI: " + response.content)
            self.messages.append(response)


import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from langfuse.client import DatasetItemClient


class EvaluationTestDataset:
    def __init__(self):
        self.dataset_name = 'assistant-data-top50'
        self.langfuse = Langfuse()

        need_answer = PromptTemplate.from_template("""
        *********
        你是AIGC课程的助教，你的工作是从学员的课堂交流中选择出需要老师回答的问题，加以整理以交给老师回答。

        课程内容:
        {outlines}
        *********
        学员输入:
        {user_input}
        *********
        如果这是一个需要老师答疑的问题，回复Y，否则回复N。
        只回复Y或N，不要回复其他内容。""")

        model = ChatOpenAI(temperature=0, model_kwargs={"seed": 42})
        parser = StrOutputParser()

        self.chain = (
                need_answer
                | model
                | parser
        )

    def simple_evaluation(output, expected_output):
        return output == expected_output

    def uploadDataset(self):
        data = []
        with open('my_annotations.jsonl', 'r', encoding='utf-8') as fp:
            for line in fp:
                example = json.loads(line.strip())
                item = {
                    "input": {
                        "outlines": example["outlines"],
                        "user_input": example["user_input"]
                    },
                    "expected_output": example["label"]
                }
                data.append(item)

        for item in tqdm(data[:50]):
            self.langfuse.create_dataset_item(
                dataset_name=self.dataset_name,
                input=item['input'],
                expected_output=item['expected_output']
            )

    def run_evaluation(self, run_name: str):
        dataset = self.langfuse.get_dataset(self.dataset_name)

        def process_item(item: DatasetItemClient):
            handler = item.get_langchain_handler(run_name=run_name)

            # Assuming chain.invoke is a synchronous function
            output = self.chain.invoke(item.input, config={"callbacks": [handler]})
            print(handler.trace.trace_id)

            # Assuming handler.root_span.score is a synchronous function
            handler.root_span.score(
                name="accuracy",
                value=self.simple_evaluation(output, item.expected_output)
            )
            print('.', end='', flush=True)

        # Using ThreadPoolExecutor with a maximum of 10 workers
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(process_item, dataset.items)


if __name__ == '__main__':
    sd = EvaluationTestDataset()
    # sd.uploadDataset()
    sd.run_evaluation('do-evaluation-4')
