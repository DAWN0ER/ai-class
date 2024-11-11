from swarm import Swarm, Agent
from openai import OpenAI
import json

'''
messages=[{'content': '1. 请简述什么是AI智能体，并列举两个实际生活中的AI智能体应用案例。\n\n2. AI智能体的工作原理是什么？请描述其基本工作流程。\n\n3. AI智能体有哪些主要类型？请分别解释其特点和应用场景。\n\n4. 在构建AI智能体时 ，会用到哪些关键技术或算法？请列举至少三种。\n\n5. 你认为未来AI智能体的发展趋势会怎样？请从技术、应用等方面进行分析。', 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': None, 'sender': 
'老师'}] 

agent=Agent(
     name='老师', 
     model='qwen-turbo', 
     instructions='你是一个老师，需要对指定的课题布置相关作业。作业以问答题为主，不超过5道题，每道题不超过100字。', 
     functions=[], 
     tool_choice=None, 
     parallel_tool_calls=True,
     context_variables={}
)
'''

msg1 = {"role":"user","content":"知识：全名：超古代怪兽哥尔赞，身高：62米，体重：6万8千吨，哥尔赞与迪迦奥特曼战斗中被打败之后，遁入地底的哥尔赞潜入雾门岳山地底，积蓄火焰岩浆能量来强化自己，使自己变为强化型的哥尔赞。强化后的哥尔赞具有比以前哥尔赞更强的实力。积蓄岩浆能量，战斗力提高的哥尔赞。头部有像盔甲一样的装甲、强韧的皮肤、尖锐的指甲、巨大的力量，配合威力强大的强化超音波光线攻击对手。 "}
msg2 = {"role":"user","content":"提问：给出哥尔赞的相关信息"}

def printResult(resp,angetName):
    print(f"Response: {resp}\n")
    ans = resp.messages[-1]["content"]
    print(f"Angent: {angetName}\nAnswer: {ans}\n")
    print("-----------------对话完成---------------------\n")

try :
    client = OpenAI(
        api_key="sk-59a6606f67394158a868a39dc6d2fe3d",
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
