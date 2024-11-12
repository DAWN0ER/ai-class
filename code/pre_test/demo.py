from swarm import Swarm, Agent
from openai import OpenAI
import json

"""
messages=[{'content': '1. 请简述什么是AI智能体，并列举两个实际生活中的AI智能体应用案例。\n\n2. AI智能体的工作原理是什么？请描述其基本工作流程。\n\n3. AI智能体有哪些主要类型？请分别解释其特点和应用场景。\n\n4. 在构建AI智能体时 
，会用到哪些关键技术或算法？请列举至少三种。\n\n5. 你认为未来AI智能体的发展趋势会怎样？请从技术、应用等方面进行分析。', 'refusal': None, 'role': 'assistant', 'audio': None, 'function_call': None, 'tool_calls': None, 'sender': 
'老师'}] agent=Agent(name='老师', model='qwen-turbo', instructions='你是一个老师，需要对指定的课题布置相关作业。作业以问答题为主，不超过5道题，每道题不超过100字。', functions=[], tool_choice=None, parallel_tool_calls=True) context_variables={}
"""


try :
    client = OpenAI(
        api_key="sk-59a6606f67394158a868a39dc6d2fe3d",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    swarm_client = Swarm(client)

    student = Agent(
        name="学生",
        instructions="你是一个学生，需要对给你的提问和作业回答问题，每个问题的答案不超过200字",
        model="qwen-turbo"
    )

    teacher = Agent(
        name="老师",
        instructions="你是一个老师，需要对指定的课题布置相关作业。作业以问答题为主，不超过5道题，每道题不超过100字。",
        model="qwen-turbo",
    )

    msg = {"role":"user","content":"今天的课题是AI智能体"}

    rsp_t = swarm_client.run(
        agent= teacher,
        messages= [msg],
    )

    ans = rsp_t.messages[-1]["content"]
    print(f"angent:{teacher.name}:\nanswer:{ans}")
    
    msg2={"role":"user","content":ans}

    rsp_s = swarm_client.run(
        agent=student,
        messages=[msg2],
    )

    ans = rsp_s.messages[-1]["content"]
    print(f"angent:{student.name}:\nanswer:{ans}")


except Exception as e:
    print(f"错误:{e}")