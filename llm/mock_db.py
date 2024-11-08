# 定义本地函数和数据库
import sqlite3

# 创建数据库连接
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

class init_db():
    def init_db_order(self):
        # 创建orders表
        cursor.execute("""
        CREATE TABLE orders (
            id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
            customer_id INT NOT NULL, -- 客户ID，不允许为空
            product_id STR NOT NULL, -- 产品ID，不允许为空
            price DECIMAL(10,2) NOT NULL, -- 价格，不允许为空
            status INT NOT NULL, -- 订单状态，整数类型，不允许为空。0代表待支付，1代表已支付，2代表已退款
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认为当前时间，格式为'YYYY-MM-DD HH:MM:SS'
            pay_time TIMESTAMP -- 支付时间，可以为空，格式为'YYYY-MM-DD HH:MM:SS'
        );
        """)

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


def ask_database(arguments):
    cursor.execute(arguments["query"])
    records = cursor.fetchall()
    return records


# 可以被回调的函数放入此字典
available_functions = {
    "ask_database": ask_database,
}