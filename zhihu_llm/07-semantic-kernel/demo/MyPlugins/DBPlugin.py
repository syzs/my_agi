from semantic_kernel.skill_definition import sk_function

class DBConnector:
    def __init__(self, db_cursor):
        self.db_cursor = db_cursor
        
    @sk_function(
        description="查询数据库", # function 描述
        name="query_database", # function 名字
    )
    def exec(self, sql_exp: str) -> str:
        self.db_cursor.execute(sql_exp)
        records = cursor.fetchall()
        return str(records)