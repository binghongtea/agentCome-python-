import asyncio
import aiofiles

async def asyncKnowledge():
    async with aiofiles.open('async_knowledge.txt','w', encoding='utf-8') as f:
        await f.write('asyncio 是 Python 异步编程的库')
        print('写入完成')

    async with aiofiles.open('async_knowledge.txt','r', encoding='utf-8') as f:
        content = await f.read()
        print(content)
        print('写入结束')

if __name__ == '__main__':
    asyncio.run(asyncKnowledge())
