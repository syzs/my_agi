import sqlite3
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from function_calling import print_json

_ = load_dotenv(find_dotenv())

client = OpenAI()

#  描述数据库表结构
database_schema_string = """
CREATE TABLE customers (
    id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
    customer_name VARCHAR(255) NOT NULL, -- 客户名，不允许为空
    email VARCHAR(255) UNIQUE, -- 邮箱，唯一
    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 注册时间，默认为当前时间
);
CREATE TABLE products (
    id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
    product_name VARCHAR(255) NOT NULL, -- 产品名称，不允许为空
    price DECIMAL(10,2) NOT NULL -- 价格，不允许为空
);
CREATE TABLE orders (
    id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
    customer_id INT NOT NULL, -- 客户ID，不允许为空
    product_id INT NOT NULL, -- 产品ID，不允许为空
    price DECIMAL(10,2) NOT NULL, -- 价格，不允许为空
    status INT NOT NULL, -- 订单状态，整数类型，不允许为空。0代表待支付，1代表已支付，2代表已退款
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认为当前时间
    pay_time TIMESTAMP -- 支付时间，可以为空
);
"""

# 创建数据库连接
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

def initBD():
    # 创建orders表
    cursor.execute(database_schema_string)

    # 插入5条明确的模拟记录
    mock_data = [
        (1, 1001, 'TSHIRT_1', 50.00, 0, '2023-10-12 10:00:00', None),
        (2, 1001, 'TSHIRT_2', 75.50, 1, '2023-10-16 11:00:00', '2023-08-16 12:00:00'),
        (3, 1002, 'SHOES_X2', 25.25, 2, '2023-10-17 12:30:00', '2023-08-17 13:00:00'),
        (4, 1003, 'HAT_Z112', 60.75, 1, '2023-10-20 14:00:00', '2023-08-20 15:00:00'),
        (5, 1002, 'WATCH_X001', 90.00, 0, '2023-10-28 16:00:00', None)
    ]

    for record in mock_data:
        cursor.execute('''
        INSERT INTO orders (id, customer_id, product_id, price, status, create_time, pay_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', record)

    # 提交事务
    conn.commit()

def ask_database(query):
    cursor.execute(query)
    records = cursor.fetchall()
    return records

def get_sql_completion(messages, model='gpt-3.5-turbo'):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        tools=[{  # 摘自 OpenAI 官方示例 https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
            "type": "function",
            "function": {
                "name": "ask_database",
                "description": "Use this function to answer user questions about business. \
                            Output should be a fully formed SQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""
                            SQL query extracting info to answer the user's question.
                            SQL should be written using this database schema:
                            {database_schema_string}
                            The query should be returned in plain text, not in JSON.
                            The query should only contain grammars supported by SQLite.
                            """,
                        }
                    },
                    "required": ["query"],
                }
            }
        }],
    )
    return response.choices[0].message

def query_multi_table():
    prompt = "统计每月每件商品的销售额"
    # prompt = "这星期消费最高的用户是谁？他买了哪些商品？ 每件商品买了几件？花费多少？"
    messages = [
        {"role": "system", "content": "基于 order 表回答用户问题"},
        {"role": "user", "content": prompt}
    ]
    response = get_sql_completion(messages)
    print(response.tool_calls[0].function.arguments)

def query_single_table():
    initBD()

    prompt = "10月的销售额"
    # prompt = "哪个用户消费最高？消费多少？"

    messages = [
        {"role": "system", "content": "基于 order 表回答用户问题"},
        {"role": "user", "content": prompt}
    ]

    response = get_sql_completion(messages)
    print_json(response)
    messages.append(response)

    if response.tool_calls is not None:
        tool_call = response.tool_calls[0]
        if tool_call.function.name == "ask_database":
            arguments = tool_call.function.arguments
            args = json.loads(arguments)
            print(f"====SQL====\n{args['query']}")
            result = ask_database(args["query"])
            print(f"====DB Records====\n{result}")

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": "ask_database",
                "content": str(result)
            })
            response = get_sql_completion(messages)
            print("====最终回复====")
            print(response.content)

if __name__ == '__main__':
    query_single_table()




