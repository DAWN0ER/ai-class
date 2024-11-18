# 初始化配置
from pre_cfg import *

from swarm import Agent
import random
import json
import uuid

extra_prompt = '''
你需要做到的额外要求如下：
强制要求：在交流的开头携带“[身份][姓名]”形式的前缀，表明身份和姓名，其他和你交流的角色也会带有相同的前缀。
要求：面对问题尽量言简意赅，避免不必要的反问和商讨，只有确实对问题又明显疑问和不明确信息的时候可以进行反问。
建议：和其他人交流时，如果对方的回答有反问，尽量回答将交流进行下去。
提示：在对话中会出现“█”这个字符，表示这一部分内容为未知的或已经损坏的信息。
'''

# 学生花名册 name:Agent
roster = dict()
# 老师列表，单成员
teacher_list = []

# 基类
class Character:

    def __init__(self, agent:Agent, forget_ratio:float, permanent:int):
        self.agent = agent
        self.forget_ratio = forget_ratio
        self.permanent = permanent
        self.content_id = agent.name + '_m.log'
        logger.info(f"[{self.agent.name}][角色初始化] name:{agent.name}, forget_ratio:{forget_ratio}, permanent:{permanent}\n[Agent_instructions]:\n{agent.instructions}")
    
    # 加载上下文
    def content_load(self) -> list:
        try:
            with open(content_dir + self.content_id, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    # 覆盖上下文
    def content_cover(self, content):
        with open(content_dir + self.content_id, 'w') as file:
            json.dump(content, file, indent=4, ensure_ascii=False)
            logger.debug(f"[{self.agent.name}][上下文记忆覆写] current_content = {content}")

    # 随机遗忘上下文
    def forget(self):
        # 过滤参数
        if(self.forget_ratio <= 0 or self.permanent <= 0):
            return
        
        logger.debug(f"[{self.agent.name}] 触发遗忘。")
        memory = self.content_load()
        if (len(memory) == 0):
            return
        cnt = 0
        for msg in memory[::-1] :
            # 永久记忆门限
            if (cnt > self.permanent):
                break
            # 系统设定不能遗忘
            if (msg["role"] == "system"):
                continue
            
            tokens = tokenizer.cut(msg["content"])
            for token in tokens:
                if(token[1] not in ["g","w","x",""] and random.random() <= self.forget_ratio):
                    token[0] = mask
            msg["content"] = ''.join([token[0] for token in tokens])
            cnt += 1
        self.content_cover(content=memory)

    # 追加上下文，表现上等同于 remember
    def remember(self, msg):
        logger.debug(f"[{self.agent.name}][添加新上下文] new_msg:{msg}")
        memory = self.content_load()
        memory.append(msg)
        self.content_cover(content=memory)

    # 基础对话交互功能
    def talk(self, content:str) -> str:
        talk_id = str(uuid.uuid1())[:23]
        logger.info(f"[{self.agent.name}][对话][{talk_id}] 对话交互开始\nQuestion:\n{content}")
        self.remember({"role":"user","content":content})
        memory = self.content_load()
        try:
            rsp = client.run(
                agent=self.agent,
                messages=memory
            )
            answer = rsp.messages[-1]["content"]
            logger.info(f"[{self.agent.name}][对话][{talk_id}] 对话交互结果\nAnswer:\n{answer}")
            self.remember({"role":"assistant","content":answer})
            return answer
        except Exception as e:
            logger.error(f"Character:{self.agent.name}, 交流出现异常:{e}!")
            return "抱歉出错了，我无法回答这个问题。"

# 学生
class Student(Character):

    def __init__(self, name:str, forget_ratio:float, permanent:int):
        new_agent = Agent(
            name=name,
            model=my_model,
            # TODO
            instructions = 
                f"你是一名学生，名字是{name}。"
                + '\n'
                + "如果你需要和班级里的其他学生交流时，可以使用 talk2 函数。"
                + "如果你需要拿到班级中的学生的花名册，可以使用 aware_roster 函数。"
                + "如果你需要询问老师问题，可以使用 ask_teacher 函数。"
                + extra_prompt,
            functions = [talk2,aware_roster,ask_teacher]
        )
        super().__init__(agent=new_agent,forget_ratio=forget_ratio,permanent=permanent)
        # 学生加入花名册
        roster[name]=self

# 老师
class Teacher(Character):

    def __init__(self, name:str):
        new_agent = Agent(
            name=name,
            model=my_model,
            # TODO
            instructions = 
                f"你是一名老师，名字是{name}。"
                + '\n'
                + "如果你需要和班级里的其他学生交流时，可以使用 talk2 函数。"
                + "如果你需要拿到班级中的学生的花名册，可以使用 aware_roster 函数。" 
                + extra_prompt,
            functions = [talk2,aware_roster],
        )
        super().__init__(agent=new_agent,forget_ratio=0,permanent=0)
        # 老师加入 list
        teacher_list.append(self)

# functions[]

# 和其他角色交流的能力
def talk2(name:str, content:str) -> str:
    """
    用于和班级里的其他学生交流。

    参数:
    name(str): 想要交谈的人名字
    content(str): 想要交谈的内容，强制要求开头携带“[身份][姓名]”形式的前缀，表明身份和姓名。

    返回值:
    str: 对方的回答
    """

    crct = roster[name]
    if(crct == None):
        logger.error(f"[Function][ask_teacher]所在的班级没有老师！期望交流内容\n{content}")
        return '[ERROR]名字出错了，没有找到这个人。'
    id,orignal = get_id_name(content=content)
    logger.debug(f"[Function][talk2] 函数被调用，调用发起方[{id}][{orignal}]，被调用方[{name}]")
    return crct.talk(content)

# 感知班级环境的能力：获取学生花名册
def aware_roster() -> list:
    """
    用于拿到班级中的学生的花名册。
    
    返回值:
    list: 班级所有学生姓名的列表
    """

    return list(roster.keys())

# 让学生和老师交流的方法
def ask_teacher(content:str) -> str:
    """
    用于和老师交流。
    
    参数: 
    content(str): 你想要交流对话的内容，强制要求开头携带“[身份][姓名]”形式的前缀，表明身份和姓名。
    
    返回值: 
    str: 对方的回应。
    """

    if(teacher_list == []):
        logger.error(f"[Function][ask_teacher]所在的班级没有老师！期望交流内容\n{content}")
        return "[ERROR]你所在的班级没有老师。"
    id,orignal = get_id_name(content=content)
    logger.debug(f"[Function][talk2] 函数被调用，调用方[{id}][{orignal}]。")
    return teacher_list[0].talk(content)