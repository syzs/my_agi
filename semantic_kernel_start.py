import json

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextEmbedding
# Plugins 最初命名为 Skills，后来改为 Plugins。但是无论文档还是代码，都还有大量的「Skill」遗留。见到后，就知道两者是一回事就好。
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
import os
import asyncio

from semantic_kernel.core_skills import (
    FileIOSkill,
    MathSkill,
    TextSkill,
    TimeSkill,
)
from semantic_kernel.planning import SequentialPlanner

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


class tell_joke:
    def __init__(self):
        self.tell_joke_about = kernel.create_semantic_function("给我讲个关于{{$input}}的笑话吧")

    async def run_function(self, context):
        return await kernel.run_async(
            self.tell_joke_about,
            input_str=context
        )

    def run_job(self, context):
        # 运行 function 看结果
        result = asyncio.run(self.run_function(context))
        print(result)


class DayOfWeek:
    def __init__(self):
        # 加载 semantic function。注意目录结构
        self.my_skill = kernel.import_semantic_skill_from_directory(
            "./skprompt", "sample")

    async def run_function(self):
        return await kernel.run_async(
            self.my_skill["DayOfWeek"],
            input_str="将系统日期设置为1993-03-27"
        )

    def run(self):
        result = asyncio.run(self.run_function())
        print(result)


class ChatHistory:
    def __init__(self):
        self.prompt_config = kernel.import_semantic_skill_from_directory("./skprompt", "sample")
        self.history = []

    async def run_function(self, variables):
        return await kernel.run_async(
            self.prompt_config['ChatHistory'],
            input_vars=variables,  # 注意这里从 input_str 改为 input_vars
        )

    def run(self):
        while True:
            request = input("User >").strip()
            if not request:
                print('System: byebye')
                break

            # 通过 ContextVariables 维护多个输入变量
            variables = sk.ContextVariables()
            variables['request'] = request
            variables['history'] = '\n'.join(self.history)

            result = asyncio.run(self.run_function(variables))

            # 将新一轮的对话加到 history 中
            self.history.append('User: ' + request)
            self.history.append('Assiatant: ' + result.result)

            print('Assiatant > ' + result.result)


'''
Native Functions
'''

'''
用编程语言写的函数，如果用 SK 的 Native Function 方式定义，就能纳入到 SK 的编排体系，可以被 Planner、其它 plugin 调用。
在 SK 中，Semantic Function 和 Native Function 被 Kernel 平等对待。
'''


class commandVerifer:
    @sk_function(
        description='检查命令是否合法',
        name='verifyCommand'
    )
    def verify(self, command: str) -> str:
        print('verify-->', command)
        if ">" in command:
            return "非法"
        parts = command.replace(';', '|').split('|')
        for cmd in parts:
            name = cmd.split(" ")[0]
            if name not in ["ls", "cat", "head", "tail", "echo"]:
                return "非法"
        return "合法"


class VeriferCommand:
    def run(self):
        # 加载 native function
        verify_skill = kernel.import_skill(commandVerifer(), "Verifier")

        # 看结果
        result = asyncio.run(kernel.run_async(
            verify_skill["verifyCommand"],
            input_str='date -s "2023-04-01"',
            # input_str="ls -l ./",
        ))

        print(result)


'''
多参数 Native Function 的写法
'''


class Math:
    @sk_function(
        description="加法",
        name="add",
    )
    @sk_function_context_parameter(
        name="number1",
        description="被加数",
    )
    @sk_function_context_parameter(
        name="number2",
        description="加数",
    )
    def add(self, context: SKContext) -> str:
        return str(float(context["number1"]) + float(context["number2"]))

    @sk_function(
        description="减法",
        name="minus",
    )
    @sk_function_context_parameter(
        name="number1",
        description="被减数",
    )
    @sk_function_context_parameter(
        name="number2",
        description="减数",
    )
    def minus(self, context: SKContext) -> str:
        return str(float(context["number1"]) - float(context["number2"]))


class MathPlugin:
    def run(self):
        # 加载 native function
        math_skill = kernel.import_skill(Math(), "Math")

        verify_skill = kernel.import_skill(commandVerifer(), "Verifier")

        # 创建 SKContext
        context = sk.ContextVariables()

        # 变量赋值
        context["number1"] = 1024
        context["number2"] = 65536

        # 看结果
        result = asyncio.run(kernel.run_async(
            math_skill["add"],
            verify_skill["verifyCommand"],  # 加法计算结果：非法
            input_vars=context
        ))
        print(f"加法计算结果：{result}")

        result = asyncio.run(kernel.run_async(
            math_skill["minus"],
            input_vars=context
        ))
        print(f"减法计算结果：{result}")


class Pipeline():
    def __init__(self):
        self.command_skill = kernel.import_semantic_skill_from_directory(
            "./skprompt", "sample")
        self.verify_skill = kernel.import_skill(commandVerifer(), "Verifier")

    '''
    先执行 command_skill 再执行 verify_skill, 按 给定的 function 顺序 串行执行
    '''

    def run(self):
        result = asyncio.run(kernel.run_async(
            self.command_skill["GenerateCommand"],
            self.verify_skill["verifyCommand"],
            # input_str="删除所有根目录文件", # 非法
            input_str="显示 example.txt 文件的内容",  # 合法
        ))
        print(result)


# 嵌套调用
class SkInnerFunction:
    def __init__(self):
        self.chat_prompt = '''
        User 和 Assistant 的对话历史摘要如下：
        {{ChatHistorySkill.summarize $history}}
        
        User: {{$request}}
        '''
        self.chat_function = kernel.create_semantic_function(
            prompt_template=self.chat_prompt)

        self.summarize_prompt = '''
        请将以下 User 与 Assistant 的对话生成一个间断的的摘要
        切包你的摘要中包含中包含完整的信息
        <dialog>
        {{$history}}
        </dialog>
        摘要：
        '''
        self.summarize_function = kernel.create_semantic_function(
            prompt_template=self.summarize_prompt,
            function_name='summarize',
            skill_name='ChatHistorySkill',
            description='Summarize a dialog history',
        )

        self.history = []

    def run(self):
        while True:
            request = input('User > ').strip()
            if not request:
                break
            variables = sk.ContextVariables()
            variables['request'] = request
            variables['history'] = '\n'.join(self.history)

            result = asyncio.run(kernel.run_async(
                self.chat_function,
                input_vars=variables,
            ))

            self.history.append('User: ' + request)
            self.history.append('Assistant: ' + result.result)

            print('Assistant: ' + result.result)

# native 嵌套调用
class SkMultiNativeFunction:
    def __init__(self):
        self.prompt = """
        将用户输入解析为函数调用

        例如：

        3加5等于多少
        {"name":"add","number1":3,"number2":5}

        一百减十等于几
        {"name":"minus","number1":100,"number2":10}

        用户输入：
        {{$input}}

        以JSON形式输出，包括一下三个字段：
        name: 函数名，必须为'add'或'minus'之一；
        number1: 参与计算的第一个数，即被加数或被减数；
        number2: 参与计算的第二个数，即加数或减数。

        不要分析，不要评论，直接输出答案。
        """

    def run(self):
        # 加载skill
        kernel.import_skill(Math(), "Math")

        # 加载 nested skills
        kernel.create_semantic_function(
            prompt_template=self.prompt,
            function_name='QueryNestedFunction',
            skill_name='ExampleSkill',
            description='将用户输入的文本转成json形式的计算表达式'
        )

        skill = kernel.import_skill(Calculator(), 'Calculator')

        result = asyncio.run(kernel.run_async(
            skill['calc'],
            input_str='100加100',
        ))
        print(result)

class Calculator:
    def __init__(self):
        pass

    @sk_function(
        description="加减计算器",
        name="calc",
    )
    async def calc(self, query:str) -> str:
        # 嵌套调用 Semantic Function
        q2f = kernel.skills.get_function("ExampleSkill", "Query2Function")
        json_str = asyncio.run(kernel.run_async(q2f, input_str=query)).result.strip()
        json_obj = json.loads(json_str)
        func_name = json_obj['name']
        context = kernel.create_new_context()
        context["number1"] = json_obj["number1"]
        context["number2"] = json_obj["number2"]
        # 嵌套调用 Native Function
        math_func = kernel.skills.get_function("Math", func_name)
        result = asyncio.run(kernel.run_async(math_func, input_context=context)).result.strip()
        return result

def verify_command_function():
    prompt = """
    已知，判断用户指令是否为合法指令的结果是：
    {{Verifier_Func.verifyCommand $input}}

    根据以上结果，执行下述动作之一：
    如果用户指令为非法，向用户说明该指令不合法；
    否则，解释该命令的用途。

    User：{{$input}}
    Assistant:
    """
    kernel.import_skill(commandVerifer(), "Verifier_Func")
    # 创建 semantic function
    semantic_function = kernel.create_semantic_function(prompt)

    result = asyncio.run(kernel.run_async(
        semantic_function,
        # input_str="ls -l *",
        input_str="rm -rf *"
    ))
    print(result.result)

from semantic_kernel.text import split_markdown_lines
class SkEmbedding:
    def __init__(self):
        self.kernel = sk.Kernel()

        # 把 LLM 服务加入 kernel
        # 可以加多个。第一个加入的会被默认使用，非默认的要被指定使用
        self.kernel.add_text_completion_service(
            "my-gpt3",
              OpenAIChatCompletion("gpt-3.5-turbo", api_key))

        # 添加 embedding 服务
        self.kernel.add_text_embedding_generation_service(
            "ada", OpenAITextEmbedding("text-embedding-ada-002", api_key))

        # 使用内存做 memory store
        self.kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())

    async def save_information(self, _kernal, index, line):
        await _kernal.memory.save_information_async('chatall', id=index, text=line)

    async def save_information_async(self, _kernal):
        # 读取文件内容
        with open('ChatALL.md', 'r') as f:
            content = f.read()

        # 将文件内容分片，单片最大 100 token（注意：SK 的 text split 功能目前对中文支持不如对英文支持得好）
        lines = split_markdown_lines(content, 100)
        # 将分片的内容存入内存
        save_info_tasks = []
        for index, line in enumerate(lines):
            save_info_tasks.append(asyncio.create_task(self.save_information(_kernal, index, line)))
        await asyncio.wait(save_info_tasks)

    async def run(self):
        # 向量数据准备
        await self.save_information_async(self.kernel)
        # 向量搜索
        result = await self.kernel.memory.search_async('chatall', 'ChatALL怎么下载？')
        print(result[0].text)

    # 用函数嵌套做一个简单的 RAG
    async def run_rag(self):
        # 向量数据准备
        await self.save_information_async(self.kernel)

        # 导入内置的 `TextMemorySkill`。主要使用它的 `recall()`
        self.kernel.import_skill(sk.core_skills.TextMemorySkill())

        # 直接在代码里创建 semantic function。真实工程不建议这么做
        # 里面调用了 `recall()`
        sk_prompt = """
        基于下面的背景信息回答问题。如果背景信息为空，或者和问题不相关，请回答"我不知道"。

        [背景信息开始]
        {{recall $input}}
        [背景信息结束]

        问题：{{$input}}
        回答：
        """
        ask = self.kernel.create_semantic_function(sk_prompt)

        # 提问
        context = self.kernel.create_new_context()
        context[sk.core_skills.TextMemorySkill.COLLECTION_PARAM] = 'chatall'
        context['input'] = 'ChatALL怎么下载？'

        result = await self.kernel.run_async(
            ask,
            input_context=context,
        )
        print(result)


class SequentialPlan:
    async def run(self):
        kernel = sk.Kernel()
        kernel.add_text_completion_service('gpt-3.5', OpenAIChatCompletion('gpt-3.5-turbo', api_key))
        kernel.import_skill(MathSkill(), 'math')
        kernel.import_skill(FileIOSkill(),'fileIO')
        kernel.import_skill(TimeSkill(), 'time')
        kernel.import_skill(TextSkill(), 'text')

        # create an instance of sequential planner
        planner = SequentialPlanner(kernel)
        ask = 'what day of the week id today, all uppercase'
        # aks the sequential planner to indentify a suitable funcion from the list of functions available
        plan = await planner.create_plan_async(goal=ask)
        # ask the sequential planner to execute the identified function
        result = await plan.invoke_async()

        print("plan steps:")
        for step in plan._steps:
            print(step.description, ":", step._state.__dict__)

        print("Expected Answer:")
        print(result)


if __name__ == '__main__':
    sp = SequentialPlan()
    # asyncio.run(se.run())
    asyncio.run(sp.run())
