import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastAPI 示例")

@app.get('/')
def get_root():
    return {"Hello": "this is smart system"}

@app.get('/user/{user_id}')
def get_user(user_id: int,name:str):
    return {"user_id": user_id, "name": name}

class UserInfo(BaseModel):
    user_id: int
    name: str
    age: int

@app.post('/userInfo')
async def post_user_info(user_info: UserInfo):
    await asyncio.sleep(1)
    return {
        "msg":f'欢迎用户 {user_info.name}，年龄为{user_info.age}岁，用户ID为{user_info.user_id}'
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
