from character import Student,Teacher
from swarm import Swarm
from openai import OpenAI

client = Swarm(
    client= OpenAI(
        api_key="sk-59a6606f67394158a868a39dc6d2fe3d",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
)

t = Teacher("张老师",client,0.1,10)

s1 = Student("张三",client,0.1,10)
s2 = Student("李四",client,0.1,10)

def tm():
    print(f"Teacher 的 memory:{t.memory}")
    print(f"张三 的 memory:{s1.memory}")
    print(f"李四 的 memory:{s2.memory}")

print("===== 实验开始 =====")
tm()
ans = t.talk("[管理员][Dawn]你们班有哪些学生，他们是怎么介绍自己的。")
# ans = s1.talk("[管理员][Dawn]介绍一下你自己。")
print(f"Answer:\n{ans}")
print("=====对话结束=====")
tm()