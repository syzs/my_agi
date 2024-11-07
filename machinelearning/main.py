'''
uvicorn main:app --reload

main: 文件main.py
app: main.py 内创建的对象app=FastAPI()
--reload: 更改代码后服务器重新启动，仅用于开发
'''

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}
