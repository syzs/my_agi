# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage,  # 等价于OpenAI接口中的assistant role
    HumanMessage,  # 等价于OpenAI接口中的user role
    SystemMessage  # 等价于OpenAI接口中的system role
)
# 其它模型分装在 langchain_community 底包中
from langchain_community.chat_models import (
    ErnieBotChat,
    QianfanChatEndpoint
)


class IOChat:
    def __init__(self):
        self.llm = ChatOpenAI(model_name='gpt-4')  # ChatOpenAI() # 默认是gpt-3.5-turbo doesnt work

    def singleDialogue(self):
        response = self.llm.invoke('which version gpt are you using')
        print(response.content)

    def multipleDialogue(self):
        messages = [
            SystemMessage(content='你是AGIClass的课程助理'),
            HumanMessage(content='我是学员，我叫女王大人'),
            AIMessage(content='欢迎！'),
            HumanMessage(content='我是谁')
        ]
        response = self.llm.invoke(messages)
        print(response.content)

    def ernieBotChat(self):  # 加载文心一言模型
        messages = [HumanMessage(content='你是谁')]
        # deprecated
        # ernie = ErnieBotChat()

        # ernie.invoke(messages)
        # no enough credential found, any one of (access_key, secret_key), (ak, sk), access_token must be provided
        qianfan = QianfanChatEndpoint()
        qianfan.invoke(messages)


from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
)
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import load_prompt


class PromptStarter:
    def __init__(self):
        self.llm = ChatOpenAI(model_name='gpt-4')  # ChatOpenAI() # 默认是gpt-3.5-turbo doesnt work

    def promptTemplate(self):
        template = PromptTemplate.from_template('给我讲一个关于{subject}的笑话')
        print(template)  # input_variables=['subject'] template='给我讲一个关于{subject}的笑话'
        print(template.format(subject='小明'))  # 给我讲一个关于小明的笑话

    def formatMessage(self):
        template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template('你是{product}的客服助手，你的名字叫{name}'),
                HumanMessagePromptTemplate.from_template('{query}')
            ]
        )

        prompt = template.format_messages(
            product='AGI课堂',
            name='guagua',
            query='你是谁'
        )
        print(prompt)  # [SystemMessage(content='你是AGI课堂的客服助手，你的名字叫guagua'), HumanMessage(content='你是谁')]

    def loadFromFile(self):
        prompt = load_prompt('langchain_prompt/simple_prompt.yaml')
        print('load from yaml:', prompt)
        message = prompt.format(adjective='funny', content='xiaoming')
        print(message)

        prompt = load_prompt('langchain_prompt/simple_prompt.json')
        print('load from json:', prompt)
        message = prompt.format(adjective='funny', content='xiaoming')
        print(message)

        prompt = load_prompt('langchain_prompt/simple_prompt_template_path.json')
        print('load from multi file:', prompt)
        message = prompt.format(adjective='funny', content='xiaoming')
        print(message)


from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List, Dict


# 定义输出对象
class OutputParserClass(BaseModel):
    year: int = Field(description='Year')
    month: int = Field(description='Month')
    day: int = Field(description='Day')
    era: str = Field(description='BC or AD')

    @staticmethod
    def is_leap_year(year):
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return True
        return False

    # ----- 可选机制 --------
    # 你可以添加自定义的校验机制
    @validator('month')
    def valid_month(cls, field):
        if field <= 0 or field > 12:
            raise ValueError("月份必须在1-12之间")
        return field

    @validator('day')
    def valid_day(cls, field):
        if field <= 0 or field > 31:
            raise ValueError("日期必须在1-31日之间")
        return field

    @validator('date', pre=True, always=True)
    def valid_date(cls, day, values):
        year = values.get('year')
        month = values.get('month')

        # 确保年份和月份都已经提供
        if year is None or month is None:
            return day  # 无法验证日期，因为没有年份和月份

        # 检查日期是否有效
        if month == 2:
            if cls.is_leap_year(year) and day > 29:
                raise ValueError("闰年2月最多有29天")
            elif not cls.is_leap_year(year) and day > 28:
                raise ValueError("非闰年2月最多有28天")
        elif month in [4, 6, 9, 11] and day > 30:
            raise ValueError(f"{month}月最多有30天")

        return day


from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser


class OutputParserStart:
    def __init__(self):
        self.model = ChatOpenAI(model_name='gpt-4', temperature=0)
        # 根据Pydantic对象的定义，构造一个OutputParser
        self.parser = PydanticOutputParser(pydantic_object=OutputParserClass)
        self.template = '''提取用户输入中的日期。
        {format_instructions}
        用户输入:
        {query}
        '''

        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=['query'],
            # 直接从OutputParser中获取输出描述，并对模板的变量预先赋值
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def parse(self):
        print("====Format Instruction=====")
        print(self.parser.get_format_instructions())
        '''
        
        ====Format Instruction=====
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"year": {"title": "Year", "description": "Year", "type": "integer"}, "month": {"title": "Month", "description": "Month", "type": "integer"}, "day": {"title": "Day", "description": "Day", "type": "integer"}, "era": {"title": "Era", "description": "BC or AD", "type": "string"}}, "required": ["year", "month", "day", "era"]}
```

        '''

        query = "2023年四月6日天气晴..."
        model_input = self.prompt.format_prompt(query=query)
        print("====Prompt=====")
        print(model_input.to_string())
        '''
        
        提取用户输入中的日期。
        The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"year": {"title": "Year", "description": "Year", "type": "integer"}, "month": {"title": "Month", "description": "Month", "type": "integer"}, "day": {"title": "Day", "description": "Day", "type": "integer"}, "era": {"title": "Era", "description": "BC or AD", "type": "string"}}, "required": ["year", "month", "day", "era"]}
```
        用户输入:
        2023年四月6日天气晴...
        
        '''

        output = self.model.invoke(model_input.to_messages())
        print("====模型原始输出=====")
        print(output)  # content='{"year": 2023, "month": 4, "day": 6, "era": "AD"}'
        print("====Parse后的输出=====")
        date = self.parser.parse(output.content)  # year=2023 month=4 day=6 era='AD'
        print(date)

    def autoFixedParse(self):
        fix_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.model)
        query = "2023年四月6日天气晴..."
        model_input = self.prompt.format_prompt(query=query)
        output = self.model.invoke(model_input.to_messages())
        print(output)  # content='{"year": 2023, "month": 4, "day": 6, "era": "AD"}'
        output = output.content.replace('4', '四月')
        try:
            date = self.parser.parse(output)
        except Exception as e:
            print("解析异常", e)
            '''
            Failed to parse OutputParserClass from completion 输出:
```
{
  "year": 2023,
  "month": 四月,
  "day": 6,
  "era": "AD"
}
```. Got: Expecting value: line 3 column 12 (char 29)'''
            date = fix_parser.parse(output)
            print("auto fixing 的结果")  # year=2023 month=4 day=6 era='AD'
            print(date)


from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.memory import ConversationTokenBufferMemory


class MemoryStarter:
    # 对话上下文：ConversationBufferMemory
    def bufferMemory(self):
        history = ConversationBufferMemory()
        history.save_context({"input": "你好啊"}, {"output": "你也好啊"})
        print(history.load_memory_variables({}))  # {'history': 'Human: 你好啊\nAI: 你也好啊'}
        history.save_context({"input": "你再好啊"}, {"output": "你又好啊"})
        print(history.load_memory_variables({}))  # {'history': 'Human: 你好啊\nAI: 你也好啊\nHuman: 你再好啊\nAI: 你又好啊'}

    # 只保留一个窗口的上下文：ConversationBufferWindowMemory
    def bufferWindowMemory(self):
        window = ConversationBufferWindowMemory(k=1)
        window.save_context({"input": "第一轮问"}, {"output": "第一轮答"})
        window.save_context({"input": "第二轮问"}, {"output": "第二轮答"})
        window.save_context({"input": "第三轮问"}, {"output": "第三轮答"})
        print(window.load_memory_variables({}))  # {'history': 'Human: 第三轮问\nAI: 第三轮答'}

    def tokenBufferMemory(self):
        memory = ConversationTokenBufferMemory(
            llm=ChatOpenAI(),  # 需要提供具体的模型用于计算token
            max_token_limit=40
        )
        memory.save_context(
            {"input": "你好啊"}, {"output": "你好，我是你的AI助手。"})
        memory.save_context(
            {"input": "你会干什么"}, {"output": "我什么都会"})
        print(memory.load_memory_variables({}))  # {'history': 'Human: 你会干什么\nAI: 我什么都会'}


from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from enum import Enum


# 输出结构
class SortEnum(str, Enum):
    data = 'data'
    price = 'price'


class OrderingEnum(str, Enum):
    ascend = 'ascend'
    descend = 'descend'


class Semantics(BaseModel):
    name: Optional[str] = Field(description="流量包名称", default=None)
    price_lower: Optional[int] = Field(description="价格下限", default=None)
    price_upper: Optional[int] = Field(description="价格上限", default=None)
    data_lower: Optional[int] = Field(description="流量下限", default=None)
    data_upper: Optional[int] = Field(description="流量上限", default=None)
    sort_by: Optional[SortEnum] = Field(description="按价格或流量排序", default=None)
    ordering: Optional[OrderingEnum] = Field(description="升序或降序排列", default=None)


class ChainExpressionLanguageStarter:
    def run(self):
        # OutputParser
        parser = PydanticOutputParser(pydantic_object=Semantics)

        # Prompt 模板
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "将用户的输入解析成JSON表示。输出格式如下：\n{format_instructions}\n不要输出未提及的字段。",
                ),
                ("human", "{query}"),
            ]
        ).partial(format_instructions=parser.get_format_instructions())

        # 模型
        model = ChatOpenAI(temperature=0)

        # LCEL 表达式
        runnable = (
                {"query": RunnablePassthrough()} | prompt | model | parser  # RunnablePassthrough 占位符
        )

        # 运行
        # name=None price_lower=None price_upper=100 data_lower=None data_upper=None sort_by=<SortEnum.data: 'data'> ordering=<OrderingEnum.descend: 'descend'>
        print(runnable.invoke("不超过100元的流量大的套餐有哪些"))

if __name__ == '__main__':
    oo = ChainExpressionLanguageStarter()
    oo.run()
