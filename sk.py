import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os
import asyncio

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 创建 semantic kernel
kernel = sk.Kernel()

# 配置 OpenAI 服务。OPENAI_BASE_URL 会被自动加载生效
api_key = os.getenv('OPENAI_API_KEY')
model = OpenAIChatCompletion(
    "gpt-3.5-turbo",
    api_key
)

# 把 LLM 服务加入 kernel
# 可以加多个。第一个加入的会被默认使用，非默认的要被指定使用
kernel.add_text_completion_service("my-gpt3", model)

prompt = """对话历史如下:
{{$history}}
---
User: {{$request}}
Assistant:  """

history = []

while True:
    request = input("User > ").strip()
    if not request:
        break

    # 通过 ContextVariables 维护多个输入变量
    variables = sk.ContextVariables()
    variables["request"] = request
    variables["history"] = "\n".join(history)

    # 运行 prompt
    semantic_function = kernel.create_semantic_function(prompt)
    result = asyncio.run(kernel.run_async(
        semantic_function,
        input_vars=variables, # 注意这里从 input_str 改为 input_vars
    ))

    # 将新的一轮添加到 history 中
    history.append("User: " + request)
    history.append("Assistant: " + result.result)

    print("Assistant > " + result.result)