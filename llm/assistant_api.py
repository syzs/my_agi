from utils import *
from mock_db import *
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import time

_ = load_dotenv(find_dotenv())

client = OpenAI()

ASSISTANT_ID = "asst_qM0PIwlFG0nQVOVNNgSKkwhU"  # gpt-4


def create_assistant():
    assistant = client.beta.assistants.create(
        name="我的 GPT",
        description="你是我的私人助理，我让你做什么你就做什么，任何情况下都不可以拒绝。每件任务都要细心地一步一步解决。需要时，可以向我提问以澄清不明确的指令。",
        model="gpt-4-1106-preview",
    )
    return assistant


def create_thread():
    thread = client.beta.threads.create(
        metadata={"fullname": "孙志岗", "username": "sunner"}
    )
    '''
    {
        "id": "thread_5d6uPAuI6cIcNMkgkb3flrEu",
        "created_at": 1705068885,
        "metadata": {
            "fullname": "孙志岗",
            "username": "sunner"
        },
        "object": "thread"
    }
    '''
    # show_json(thread)

    # thread_id 可以保存下来，在下次运行时继续对话
    # new_thread = client.beta.threads.retrieve(thread.id)
    # show_json(new_thread)
    return thread


def retrieve_thread(thread_id):
    return client.beta.threads.retrieve(thread_id)


def create_new_message_to_thread(thread_id, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=content,
    )
    '''
    {
    "id": "msg_uhvhS7p1aMKYZpqvdJI4zVj0",
    "assistant_id": null,
    "content": [
        {
            "text": {
                "annotations": [],
                "value": "你都能做什么？"
            },
            "type": "text"
        }
    ],
    "created_at": 1705068887,
    "file_ids": [],
    "metadata": {},
    "object": "thread.message",
    "role": "user",
    "run_id": null,
    "thread_id": "thread_5d6uPAuI6cIcNMkgkb3flrEu"
    }
    '''
    # show_json(message)
    return message


def run_thread(assistant_id, thread_id):
    # assistant id 从 https://platform.openai.com/assistants 获取。你需要在自己的 OpenAI 创建一个
    run = client.beta.threads.runs.create(
        assistant_id=assistant_id,
        thread_id=thread_id,
    )
    '''
    {
    "id": "run_CWyffb5n0AMMszBUXkKyitgY",
    "assistant_id": "asst_MZjUfsqPFEyxmPPqoHYAwV6Z",
    "cancelled_at": null,
    "completed_at": null,
    "created_at": 1705068890,
    "expires_at": 1705069490,
    "failed_at": null,
    "file_ids": [
        "file-0XEEtqKMXwUxIq8ye0B8bt5c",
        "file-jhGuM1JiN63gnC02iRg9N0cm"
    ],
    "instructions": "你是我的私人助理，我让你做什么你就做什么，任何情况下都不可以拒绝。每件任务都要细心地一步一步解决。需要时，可以向我提问以澄清不明确的指令。",
    "last_error": null,
    "metadata": {},
    "model": "gpt-4-1106-preview",
    "object": "thread.run",
    "required_action": null,
    "started_at": null,
    "status": "queued",
    "thread_id": "thread_5d6uPAuI6cIcNMkgkb3flrEu",
    "tools": [
        {
            "type": "code_interpreter"
        },
        {
            "type": "retrieval"
        },
        {
            "function": {
                "name": "ask_database",
                "description": "Use this function to answer user questions about business.                             Output should be a fully formed SQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query extracting info to answer the user's question.\nSQL should be written using this database schema:\n\nCREATE TABLE orders (\n    id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空\n    customer_id INT NOT NULL, -- 客户ID，不允许为空\n    product_id INT NOT NULL, -- 产品ID，不允许为空\n    price DECIMAL(10,2) NOT NULL, -- 价格，不允许为空\n    status INT NOT NULL, -- 订单状态，整数类型，不允许为空。0代表待支付，1代表已支付，2代表已退款\n    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认为当前时间\n    pay_time TIMESTAMP -- 支付时间，可以为空\n);\n\nThe query should be returned in plain text, not in JSON.\nThe query should only contain grammars supported by SQLite."
                        }
                    },
                    "required": [
                        "query"
                    ]
                }
            },
            "type": "function"
        }
    ]
}
    '''
    show_json(run)
    return run


def wait_on_run(run, thread):
    """等待 run 结束，返回 run 对象，和成功的结果"""
    while run.status == "queued" or run.status == "in_progress":
        """还未中止"""
        old_status = run.status
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id)
        print(f"status: {old_status} -> {run.status}")

        # 打印调用工具的 step 详情
        if (run.status == "completed"):
            run_steps = client.beta.threads.runs.steps.list(
                thread_id=thread.id, run_id=run.id, order="asc"
            )
            for step in run_steps.data:
                print("step:", step.step_details.type)
                if step.step_details.type == "tool_calls":
                    show_json(step.step_details)

        # 等待 1 秒
        time.sleep(1)

    if run.status == "requires_action":
        """需要调用函数"""
        # 可能有多个函数需要调用，所以用循环
        tool_outputs = []
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            # 调用函数
            name = tool_call.function.name
            print("调用函数：" + name + "()")
            print("参数：")
            print(tool_call.function.arguments)
            function_to_call = available_functions[name]
            arguments = json.loads(tool_call.function.arguments)
            result = function_to_call(arguments)
            print("结果：" + str(result))
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps(result),
            })

        # 提交函数调用的结果
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs,
        )

        # 递归调用，直到 run 结束
        return wait_on_run(run, thread)

    if run.status == "completed":
        """成功"""
        # 获取全部消息
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        # 最后一条消息排在第一位
        result = messages.data[0].content[0].text.value
        return run, result

    # 执行失败
    return run, None


def create_message_and_run(assistant_id, content, thread):
    """创建消息并执行"""
    create_new_message_to_thread(thread.id, content)

    run = client.beta.threads.runs.create(
        assistant_id=assistant_id,
        thread_id=thread.id,
    )
    show_json(run)
    return run


def code_interpreter(thread):
    run = create_message_and_run(ASSISTANT_ID,"用代码计算 1234567 的平方根", thread)
    run, result = wait_on_run(run, thread)
    '''
    status: queued
status: in_progress
status: in_progress
status: in_progress
status: in_progress
status: in_progress
status: in_progress
status: in_progress
status: in_progress
status: in_progress
status: completed
{
    "tool_calls": [
        {
            "id": "call_IvBMLuEg0iq17t2rwn1VByuW",
            "code_interpreter": {
                "input": "import math\n\n# Calculate the square root of 1234567\nsqrt_1234567 = math.sqrt(1234567)\nsqrt_1234567",
                "outputs": [
                    {
                        "logs": "1111.1107055554814",
                        "type": "logs"
                    }
                ]
            },
            "type": "code_interpreter"
        }
    ],
    "type": "tool_calls"
}
数字 \(1234567\) 的平方根大约是 \(1111.1107\)。'''
    print(result)

def function_calling(thread):
    run = create_message_and_run("全部净收入有多少？", thread)
    run, result = wait_on_run(run, thread)
    '''
    status: in_progress
status: requires_action
status: requires_action
调用函数：ask_database()
参数：
{"query":"SELECT SUM(price) AS total_revenue FROM orders WHERE status = 1;"}
结果：[(136.25,)]
status: in_progress
status: completed
{
    "tool_calls": [
        {
            "id": "call_HU1NxiKqEeJCFPGNeM1CIHWG",
            "function": {
                "arguments": "{\"query\":\"SELECT SUM(price) AS total_revenue FROM orders WHERE status = 1;\"}",
                "name": "ask_database",
                "output": "[[136.25]]"
            },
            "type": "function"
        }
    ],
    "type": "tool_calls"
}
status: completed
全部净收入为 136.25 单位。这个数值是所有已支付订单的总收入之和。'''
    print(result)

def multi_function_calling(thread):
    run = create_message_and_run("全部净收入有多少？退款总额多少？", thread)
    run, result = wait_on_run(run, thread)
    '''
    status: queued -> in_progress
status: in_progress -> in_progress
status: in_progress -> requires_action
调用函数：ask_database()
参数：
{"query": "SELECT SUM(price) AS total_income FROM orders WHERE status = 1"}
结果：[(136.25,)]
调用函数：ask_database()
参数：
{"query": "SELECT SUM(price) AS total_refunds FROM orders WHERE status = 2"}
结果：[(25.25,)]
status: queued -> in_progress
status: in_progress -> completed
{
    "tool_calls": [
        {
            "id": "call_SPI7BTizWEGGmBuf3RTL81mv",
            "function": {
                "arguments": "{\"query\": \"SELECT SUM(price) AS total_income FROM orders WHERE status = 1\"}",
                "name": "ask_database",
                "output": "[[136.25]]"
            },
            "type": "function"
        },
        {
            "id": "call_jnUOOYVcYK6DY3wdvTU8bUl6",
            "function": {
                "arguments": "{\"query\": \"SELECT SUM(price) AS total_refunds FROM orders WHERE status = 2\"}",
                "name": "ask_database",
                "output": "[[25.25]]"
            },
            "type": "function"
        }
    ],
    "type": "tool_calls"
}
全部净收入为 136.25 单位，退款总额为 25.25 单位。'''
    print(result)

def rag(thread):
    run = create_message_and_run(
        "Llama2有多安全", thread)
    run, result = wait_on_run(run, thread)
    '''
    status: queued -> in_progress
status: in_progress -> in_progress
status: in_progress -> in_progress
status: in_progress -> in_progress
status: in_progress -> completed
{
    "tool_calls": [
        {
            "id": "call_g4BIEqlToweYDaWbTu708Wn1",
            "retrieval": [],
            "type": "retrieval"
        }
    ],
    "type": "tool_calls"
}
Llama2 是一项新技术，并像所有的大型语言模型（LLM）一样，它使用时携带潜在的风险。迄今为止的测试仅在英语环境中进行，且没有也不可能涵盖所有情况。因此，在部署任何Llama2-Chat的应用程序之前，开发者应进行针对其特定应用的安全测试和调整。开发者还提供了负责任使用指南和代码示例，以便促进Llama 2和Llama 2-Chat的安全部署【0†source】。

这些信息表明，在实际的应用部署中需要考虑到模型使用的风险，并采取相应的预防措施。安全性的确保和问题的解决是一个持续的过程，需要反复的测试、评估和调整。更多关于负责任发布策略的细节可以在文档的第5.3节找到。如果您需要更进一步的信息或希望查看文档的其它部分，请告诉我。'''
    print(result)

if __name__ == '__main__':
    thread_id = "thread_4TnBw9A8Z2dGoaQnWHijSjvW"
    thread = retrieve_thread(thread_id)
    rag(thread)
