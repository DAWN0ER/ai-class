from swarm import Swarm, Agent
from openai import OpenAI

api_key = open("./code/api_key.cfg").readline()

try :
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    swarm_client = Swarm(client)

    student = Agent(
        name="学生",
        instructions="你是一个学生，需要对给你的提问和作业回答问题，每个问题的答案不超过100字",
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