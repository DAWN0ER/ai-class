from swarm import Agent,Swarm
import thulac
import random

# 文件静态内容
my_model = "qwen-long"
mask = "█"
# 学生花名册 name:Agent
roster = dict()
teacher_list = []

print("============加载分词器============")
tokenizer = thulac.thulac(
    seg_only = False,
    filt = False
)
print("============加载完成============")

extra_prompt = '''你需要做到的额外要求如下：
强制要求：在交流的开头携带“[身份][姓名]”形式的前缀，表明身份和姓名，其他和你交流的角色也会带有相同的前缀。
'''

# 基类
class Character:

    def __init__(self, anget:Agent, client:Swarm, forget_ratio:float, permanent:int):
        self.__agent = anget
        self.__client = client
        self.forget_ratio = forget_ratio
        self.permanent = permanent
        self.memory = []
    
    def forget(self):
        if (len(self.memory) == 0):
            return
        cnt = 0
        for msg in self.memory :
            if (cnt > self.permanent):
                break
            if (msg["role"] == "system"):
                continue

            tokens = tokenizer.cut(msg["content"])
            for token in tokens:
                if(token[1] not in ["g","w","x",""] and random.random() <= self.forget_ratio):
                    token[0] = mask
            msg["content"] = ''.join([token[0] for token in tokens])
            cnt += 1

    def __remember(self, msg):
        self.memory.append(msg)

    def talk(self, content:str) -> str:
        self.__remember({"role":"user","content":content})
        try:
            rsp = self.__client.run(
                agent=self.__agent,
                messages=self.memory
            )
            answer = rsp.messages[-1]["content"]
            self.__remember({"role":"assistant","content":answer})
            return answer
        except Exception as e:
            print(f"Character:{self.__agent.name}, 交流出现异常:{e}!")
            return "抱歉出错了，我无法回答这个问题。"

# 学生
class Student(Character):

    def __init__(self, name:str, client:Swarm, forget_ratio:float, permanent:int):
        new_agent = Agent(
            name=name,
            model=my_model,
            # TODO
            instructions = 
                "你是一名学生，名字是" + name
                + "如果你需要和班级里的其他学生交流时，可以使用 talk2 函数。"
                + "如果你需要拿到班级中的学生的花名册，可以使用 aware_roster 函数。"
                + "如果你需要询问老师问题，可以使用 ask_teacher 函数。"
                + extra_prompt,
            functions = [talk2,aware_roster,ask_teacher]
        )
        super().__init__(
            anget=new_agent,
            client=client,
            forget_ratio=forget_ratio,
            permanent=permanent
        )
        # 学生加入花名册
        roster[name]=self

    def talk(self, content:str) -> str:
        super().forget()
        return super().talk(content=content)
    
# 老师
class Teacher(Character):

    def __init__(self, name:str, client:Swarm, forget_ratio:float, permanent:int):
        new_agent = Agent(
            name=name,
            model=my_model,
            # TODO
            instructions = 
                "你是一名老师，名字是" + name
                + "如果你需要和班级里的其他学生交流时，可以使用 talk2 函数。"
                + "如果你需要拿到班级中的学生的花名册，可以使用 aware_roster 函数。" 
                + extra_prompt,
            functions = [talk2,aware_roster],
        )
        super().__init__(
            anget=new_agent,
            client=client,
            forget_ratio=forget_ratio,
            permanent=permanent
        )
        # 老师加入 list
        teacher_list.append(self)
    
# functions[]
# 和其他角色交流的能力
def talk2(name:str, content:str) -> str:
    """
    和班级里的其他学生交流的函数。

    参数:
    name(str): 想要交谈的人名字
    content(str): 想要交谈的内容，强制要求开头携带“[身份][姓名]”形式的前缀，表明身份和姓名。

    返回值:
    str: 对方的回答
    """

    crct = roster[name]
    if(crct == None):
        return '名字出错了，没有找到这个人。'
    return crct.talk(content)

# 感知班级环境的能力：获取学生花名册
def aware_roster() -> list:
    """
    拿到班级中的学生的花名册。
    
    返回值:
    list: 班级所有学生姓名的列表
    """

    return list(roster.keys())

def ask_teacher(content:str) -> str:
    """
    用于询问老师问题。
    
    参数: 
    content(str): 想要询问的内容，强制要求开头携带“[身份][姓名]”形式的前缀，表明身份和姓名。
    
    返回值: 
    str: 对方的回答。
    """

    if(teacher_list == []):
        return "你所在的班级没有老师。"
    return teacher_list[0].talk(content)