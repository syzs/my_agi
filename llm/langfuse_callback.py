from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langfuse.callback import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())


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

if __name__ == '__main__':
    langchainCallback()