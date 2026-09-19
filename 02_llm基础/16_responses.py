import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
client=OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
)
text = """黄昏时分，天边的云被晚霞染成了橘红色，像一幅徐徐展开的画卷。我习惯性地走到窗边，推开那扇有些老旧的窗，让晚风带着草木的气息涌进来。楼下传来孩子们追逐的笑闹声，远处有人家亮起了灯，一点一点，像是夜空里渐渐浮现的星星。

桌上的茶已经凉了，我重新烧了一壶水，又给自己续上一杯。茶叶在沸水里慢慢舒展，沉下去，又浮上来，像是每一个平凡的日子，看似相同，其实各有各的滋味。我坐在窗边，什么都不想做，只是看着天色一点点暗下去，看路灯次第亮起，看行人匆匆走过又消失在街角。

忽然想起小时候，夏天的夜晚总是很长。院子里摆着竹床，奶奶摇着蒲扇，给我们讲那些翻来覆去的故事。蝉声聒噪，星光却很亮，我们在院子里追着萤火虫跑，跑得满头大汗，却觉得快乐是那样简单。那时候总觉得日子过得太慢，盼着长大，盼着远方，盼着那些书本里描写的美好未来。

后来真的长大了，才明白时光是溜得最快的那个。忙忙碌碌的日子，像被按了快进键，一转眼就是一年。我们习惯了在手机里看世界，却常常忘了抬头看看真实的天空；我们记得住几千个陌生人的动态，却常常忘记问候身边最亲近的人。我们总是赶着去下一个地方，做下一件事，却很少问自己：此刻，我真的开心吗？

其实生活的好，往往就藏在那些不起眼的角落里。清晨菜市场里带着露水的青菜，午后树荫下打盹的猫，傍晚归家时亮着的那盏灯，深夜加班时同事递过来的一杯热咖啡。这些细碎的小事，单独看似乎微不足道，连成一片，却构成了我们生命里最踏实的部分。

我们总在追求那些宏大的意义，好像只有做成大事，人生才算没有白过。可是回过头来看，真正让我们记住的，往往不是那些高光时刻，而是那些平淡到几乎被忽略的瞬间。是一次突如其来的拥抱，是一场久违的雨，是一顿家人围坐的晚餐，是朋友在低谷时的一句 “我在”。

人生这趟旅程，说长不长，说短不短。我们不必每一步都跑得飞快，偶尔慢下来，也是一种前进。就像爬山，一直埋头赶路的人，往往错过了沿途的风景；而那些走走停停的人，反而把每一段山路都记在了心里。

所以，请允许自己在某个黄昏，什么都不做，只是发一会儿呆；允许自己在某个周末，放下所有计划，睡到自然醒；允许自己在某个下雨的午后，捧一本书，听雨声敲打屋檐。这些看似 “浪费” 的时光，其实是在给心灵充电，让我们有力量继续往前走。

窗外的夜色已经完全降临了，路灯把树影拉得很长。我端起那杯茶，喝了一口，温度刚刚好。远处的灯火依旧闪烁，像是一双双温暖的眼睛，注视着每一个赶路的人。我轻轻合上窗，关掉客厅的大灯，只留一盏小夜灯，在微光里写下一段话，然后对自己说：今天很好，明天继续。

愿你也能在匆忙的世界里，留一点时间给自己，慢一点，再慢一点，去感受风的方向，去聆听心底的声音。毕竟，人生最好的风景，从来不在终点，而在路上。"""
response = client.responses.create(
    model="doubao-seed-2-1-pro-260628",
    input=[
        {"role": "system", 
        "content": [
            {"type": "input_text", "text": "你是名文学助手，请根据以下问题对内容进行分析。" + text}
        ]}
    ],
    extra_body={"caching": {
        "type": "enabled",
        "prefix": True,
    }},
)

# print(response.model_dump_json(indent=2,ensure_ascii=False))
print(response.usage.model_dump_json(indent=2, ensure_ascii=False))

secondRes = client.responses.create(
    model="doubao-seed-2-1-pro-260628",
    input=[
        {"role": "user", 
        "content": [
            {"type": "input_text", "text": "这段文字的重点分析出三点"}
        ]
        }
    ],
    previous_response_id=response.id,
    extra_body={"caching": {
        "type": "enabled"
    }},
)
print(secondRes.output_text)
print(secondRes.usage.model_dump_json(indent=2, ensure_ascii=False))
