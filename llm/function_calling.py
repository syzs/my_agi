import json

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import math
import requests

amap_key = "6d672e6194caa3b639fccf2caf06c342"

_ = load_dotenv(find_dotenv())

client = OpenAI()


def print_json(data):
    """
    打印参数。如果参数是有结构的（如字典或列表），则以格式化的 JSON 形式打印；
    否则，直接打印该值。
    """
    if hasattr(data, 'model_dump_json'):
        data = json.loads(data.model_dump_json())

    if (isinstance(data, (list, dict))):
        print(json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ))
    else:
        print(data)


def get_completion_with_single_function(messages, model="gpt-3.5-turbo"):  # gpt-4-1106-preview
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,  # 模型输出的随机性，0表示随机性最小
        tools=[{  # 用 JSON 描述函数。可以定义多个。由大模型决定调用谁。也可能都不调用
            "type": "function",
            "function": {
                "name": "cal_sum",
                "description": "加法器，计算一组数的和",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                }
            }
        }],
    )
    return response.choices[0].message


def handle_single_function():
    prompt = "tell me the sum of 1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
    prompt = "桌上有 2 个苹果，四个桃子和 3 本书，一共有几个水果？"
    prompt = "give me the result of 1024*1024"  # tool_calls = "cal_sum" why ??? model 升级到 gpt-4-1106-preview 后即解决

    messages = [
        {"role": "system", "content": "你是一个数学家"},
        {"role": "user", "content": prompt}
    ]
    response = get_completion_with_single_function(messages)
    # tool_calls = [ChatCompletionMessageToolCall(id='call_btJ8eEPQcxWSkhcY9tswgfNp', function=Function(arguments='{\n  "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n}', name='cal_sum'), type='function')]
    print(f'response.content = {response.content} \ntool_calls = {response.tool_calls}')

    # ！！！！！ 把大模型的回复加入到对话历史中 ！！！！！
    messages.append(response)

    if response.tool_calls is not None:
        tool_call = response.tool_calls[0]
        if tool_call.function.name == "cal_sum":
            args = json.loads(tool_call.function.arguments)
            result = sum(args["numbers"])
            print("函数调用 result:", result)

            # ！！！！！把函数调用结果加入到对话历史中！！！！！
            messages.append(
                {
                    "tool_call_id": tool_call.id,  # 用于标识函数调用的 ID
                    "role": "tool",
                    "name": "cal_sum",
                    "content": str(result)  # 数值 result 必须转成字符串
                }
            )

            # 再次调用大模型
            print("=====最终回复=====")
            response = get_completion_with_single_function(messages)
            print(f'response.content = {response.content} \ntool_calls = {response.tool_calls}')
    else:
        print("-----no tool_calls-----")


def get_location_coordinate(location, city):
    url = f"https://restapi.amap.com/v5/place/text?key={amap_key}&keywords={location}&region={city}"
    print(url)
    r = requests.get(url)
    result = r.json()
    if "pois" in result and result["pois"]:
        return result["pois"][0]
    return None


def search_nearby_pois(longitude, latitude, keyword):
    url = f"https://restapi.amap.com/v5/place/around?key={amap_key}&keywords={keyword}&location={longitude},{latitude}"
    print(url)
    r = requests.get(url)
    result = r.json()
    ans = ""
    if "pois" in result and result["pois"]:
        for i in range(min(3, len(result["pois"]))):
            name = result["pois"][i]["name"]
            address = result["pois"][i]["address"]
            distance = result["pois"][i]["distance"]
            ans += f"{name}\n{address}\n距离：{distance}米\n\n"
    return ans


def get_completion_with_multi_funcion(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
        seed=1024,  # 随机种子保持不变，temperature 和 prompt 不变的情况下，输出就会不变
        tool_choice="auto",  # 默认值，由 GPT 自主决定返回 function call 还是返回文字回复。也可以强制要求必须调用指定的函数，详见官方文档
        tools=[{
            "type": "function",
            "function": {

                "name": "get_location_coordinate",
                "description": "根据POI名称，获得POI的经纬度坐标",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "POI名称，必须是中文",
                        },
                        "city": {
                            "type": "string",
                            "description": "POI所在的城市名，必须是中文",
                        }
                    },
                    "required": ["location", "city"],
                }
            }
        },
            {
                "type": "function",
                "function": {
                    "name": "search_nearby_pois",
                    "description": "搜索给定坐标附近的poi",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "longitude": {
                                "type": "string",
                                "description": "中心点的经度",
                            },
                            "latitude": {
                                "type": "string",
                                "description": "中心点的纬度",
                            },
                            "keyword": {
                                "type": "string",
                                "description": "目标poi的关键字",
                            }
                        },
                        "required": ["longitude", "latitude", "keyword"],
                    }
                }
            }],
    )
    return response.choices[0].message


def handle_multi_function():
    # prompt = "我想在五道口附近喝咖啡，给我推荐几个"
    prompt = "我到北京出差，给我推荐三里屯的酒店，和五道口附近的咖啡"

    messages = [
        {"role": "system", "content": "你是一个地图通，你可以找到任何地址。"},
        {"role": "user", "content": prompt}
    ]

    response = get_completion_with_multi_funcion(messages)
    # ！！！！！ 把大模型的回复加入到对话中 !!!!!
    messages.append(response)
    '''
    {
        "content": null,
        "role": "assistant",
        "function_call": null,
        "tool_calls": [
            {
                "id": "call_6UL6arSSXFmbgme79zMwVS6l",
                "function": {
                    "arguments": "{\n  \"location\": \"五道口\",\n  \"city\": \"北京\"\n}",
                    "name": "get_location_coordinate"
                },
                "type": "function"
            }
        ]
    }
    '''
    # print_json('1', response)

    cycle_index = 0
    while response.tool_calls is not None:
        all_tool_calls = []
        for tool_call in response.tool_calls:
            all_tool_calls.append(tool_call.function.name)
        cycle_index += 1
        # 1 all_tool_calls: ['get_location_coordinate']
        # 3 all_tool_calls: ['search_nearby_pois']
        print(cycle_index, 'all_tool_calls:', all_tool_calls)

        for tool_call in response.tool_calls:
            args = json.loads(tool_call.function.arguments)
            if (tool_call.function.name == "get_location_coordinate"):
                cycle_index += 1
                # 2 Call: get_location_coordinate args: {'location': '五道口', 'city': '北京'}
                print(cycle_index, "Call: get_location_coordinate args:", args)
                result = get_location_coordinate(**args)
            elif (tool_call.function.name == "search_nearby_pois"):
                cycle_index += 1
                # 4 Call: search_nearby_pois args: {'longitude': '116.337742', 'latitude': '39.992894',
                print(cycle_index, "Call: search_nearby_pois args:", args)
                result = search_nearby_pois(**args)
            else:
                cycle_index += 1
                print(cycle_index, "no tool_call matched")
            # 2 tool_call response: {'parent': '', 'address': '(在建)13A号线;13号线', 'distance': '', 'pcode': '110000', 'adcode': '110108',
            # 4 tool_call response: xxxx
            print(cycle_index, "tool_call response:", result)
            messages.append({
                "tool_call_id": tool_call.id,  # 用于标识函数调用的 ID
                "role": "tool",
                "name": tool_call.function.name,
                "content": str(result)  # 数值result 必须转成字符串
            })
        response = get_completion_with_multi_funcion(messages)
        messages.append(response)  # 把大模型的回复加入到对话中

    print("=====最终回复=====")
    print(response.content)


def get_completion_with_json(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
        tools=[{
            "type": "function",
            "function": {
                "name": "add_contact",
                "description": "添加联系人",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "联系人姓名"
                        },
                        "address": {
                            "type": "string",
                            "description": "联系人地址"
                        },
                        "tel": {
                            "type": "string",
                            "description": "联系人电话"
                        },
                    }
                }
            }
        }],
    )
    return response.choices[0].message


def handle_with_json():
    prompt = "帮我寄给王卓然，地址是北京市朝阳区亮马桥外交办公大楼，电话13012345678。"
    messages = [
        {"role": "system", "content": "你是一个联系人录入员。"},
        {"role": "user", "content": prompt}
    ]
    response = get_completion_with_json(messages)
    print("====GPT回复====")
    print_json(response)
    args = json.loads(response.tool_calls[0].function.arguments)
    print("====函数参数====")
    print_json(args)


def get_completion_with_json_mode(messages, model="gpt-3.5-turbo-1106"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message


def handle_with_json_mode():
    prompt = "帮我寄给王卓然，地址是北京市朝阳区亮马桥外交办公大楼，电话13012345678。"
    messages = [
        {"role": "system", "content": "你是一个联系人录入员。已json格式输出联系人信息"},
        {"role": "user", "content": prompt}
    ]
    response = get_completion_with_json_mode(messages)
    print("====GPT回复====")
    print_json(response)
    print_json(response.content)


def get_completion_stream(messages, model="gpt-3.5-turbo"):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        tools=[{
            "type": "function",
            "function": {
                "name": "sum",
                "description": "计算一组数的加和",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                }
            }
        }],
        stream=True,  # 启动流式输出
    )


def handle_with_stream():
    prompt = "1+2+3"
    messages = [
        {"role": "system", "content": "你是一个小学数学老师，你要教学生加法"},
        {"role": "user", "content": prompt}
    ]
    response = get_completion_stream(messages)
    function_name, args, text = '', '', ''

    print("===streaming===")

    for msg in response:
        delta = msg.choices[0].delta
        if delta.tool_calls:
            if not function_name:
                function_name = delta.tool_calls[0].function.name
            args_delta = delta.tool_calls[0].function.arguments
            print('1', args_delta)  # 打印每次得到的数据
            args += args_delta
        elif delta.content:
            text_delta = delta.content
            print('2', text_delta)
            text += text_delta
    print("===done===")
    if function_name or args:
        print("ff")
        print(function_name)
        print(args)
    if text:
        print('tt')
        print(text)


if __name__ == '__main__':
    # handle_single_function()
    # handle_multi_function()
    # handle_with_json()
    # handle_with_json_mode()
    handle_with_stream()
