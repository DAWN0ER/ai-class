from swarm import Agent,Swarm
import thulac
import random

# 文件静态内容
my_model = "qwen-long"
mask = "█"
clazz = dict()

print("============加载分词器============")
tokenizer = thulac.thulac(
    seg_only = False,
    filt = False
)
print("============加载完成============")

class Character:

    def __init__(self, anget:Agent, client:Swarm, forget_ratio:float, permanent:int):
        self.__agent = anget
        self.__client = client
        self.forget_ratio = forget_ratio
        self.permanent = permanent
        self.__memory = []
        clazz[anget.name]=self
    
    def __forget(self):
        if (len(self.__memory) == 0):
            return
        cnt = 0
        for msg in self.__memory :
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
        self.__memory.append(msg)

    def talk(self, content:str) -> str:
        self.__forget()
        self.__remember({"role":"user","content":content})
        rsp = self.__client.run(
            agent=self.__agent,
            messages=self.__memory
        )
        answer = rsp.messages[-1]["content"]
        self.__remember({"role":"assistant","content":answer})
        return answer
    
    def self_intro(self):
        print(f"{self.__agent.name}! 到!")

class Student(Character):

    def __init__(self, name:str, client:Swarm, forget_ratio:float, permanent:int):
        new_agent = Agent(
            name=name,
            model=my_model,
            instructions = "你是一名学生", # TODO
            functions=[],
            tool_choice="",
        )
        super().__init__(
            anget=new_agent,
            client=client,
            forget_ratio=forget_ratio,
            permanent=permanent
        )
    
class Teacher(Character):

    def __init__(self, name:str, client:Swarm, forget_ratio:float, permanent:int):
        new_agent = Agent(
            name=name,
            model=my_model,
            instructions = "你是一名老师", # TODO
            functions=[],
            tool_choice="",
        )
        super().__init__(
            anget=new_agent,
            client=client,
            forget_ratio=forget_ratio,
            permanent=permanent
        )
    
def getClazz() -> dict:
    return clazz