from swarm import Swarm, Agent
from openai import OpenAI
import json

msg1 = {"role":"user","content":"知识：全名：超古代怪兽哥尔赞，身高：62米，体重：6万8千吨，哥尔赞与迪迦奥特曼战斗中被打败之后，遁入地底的哥尔赞潜入雾门岳山地底，积蓄火焰岩浆能量来强化自己，使自己变为强化型的哥尔赞。强化后的哥尔赞具有比以前哥尔赞更强的实力。积蓄岩浆能量，战斗力提高的哥尔赞。头部有像盔甲一样的装甲、强韧的皮肤、尖锐的指甲、巨大的力量，配合威力强大的强化超音波光线攻击对手。 "}
msg2 = {"role":"user","content":"提问：给出哥尔赞的相关信息"}

def printResult(resp,angetName):
    print(f"Response: {resp}\n")
    ans = resp.messages[-1]["content"]
    print(f"Angent: {angetName}\nAnswer: {ans}\n")
    print("-----------------对话完成---------------------\n")

api_key = open("./code/api_key.cfg").readline()

try :
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    swarm_client = Swarm(client)

    my_agent = Agent(
        name="知识助手",
        instructions="你是一个知识助手，接下来的对话会告诉你一系列你需要记住的知识点，学习知识时只需要回答“了解”就可以。然后会有提问，请你根据你记忆的知识点推理回答。 ",
        model="qwen-long"
    )

    print(f"Msg={msg1}")
    rsp_1 = swarm_client.run(
        agent= my_agent,
        messages= [msg1],
    )
    printResult(resp=rsp_1,angetName=my_agent.name)

    print(f"Msg={[msg1,msg2]}")
    rsp_2 = swarm_client.run(
        agent=my_agent,
        messages=[msg1,msg2],
    )
    printResult(resp=rsp_2,angetName=my_agent.name)

except Exception as e:
     print(f"错误:{e}")
