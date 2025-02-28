# 初始化配置
from domain.pre_cfg import *
import domain.labtools as lab

from swarm import Agent
import random, json, uuid, thulac

extra_prompt = """
你还需遵守以下规则：

**强制要求**：格式化要求！对话，交流，提问，总结的内容的开头必须携带“[身份][姓名]”形式的前缀（例如"[学生][张三]")，表明身份和姓名，其他和你交流的角色也会带有相同的前缀，请在所有回答中严格遵循此格式。

**强制要求**：必须根据自己对话上下文得内容进行回答，不允许虚构和假设在会话中没发生过的经历。

**建议**：面对问题尽量言简意赅，避免不必要的反问或讨论，只有确实对问题又明显疑问和不明确信息的时候可以进行反问。

**建议**：在与他人交流过程中，如果遇到对方使用反问句式进行提问或表达观点时，尽量直接回答问题的核心内容，避免同样采用反问形式回应。这样做有助于保持对话的流畅性和建设性，同时也能展现出你对对方意见的尊重和理解。

**强制要求**：在处理对话内容时，如果遇到字符'█'，这表示该部分内容是未知的或是已经损坏的信息。对于这些标记为'█'的部分，请直接忽略，并且在最终输出中不要包含这个字符。

**强制要求**：请确保在回答中，所有数学公式都使用 LaTeX 格式。如果需要独立的公式块，请使用 `$$` 包裹，如果需要行内公式，请使用 `$` 包裹。请在所有回答中严格遵循此格式。
"""

# 学生花名册 name:Agent
roster = dict()
# 老师列表，单成员
teacher_list = []
# 分词器
logger.info("[分词器] loading...")
tokenizer = thulac.thulac(seg_only=False, filt=False)
logger.info("[分词器] completed...")
# 分别用不同的模型，后续如果有必要会使用 deepseek
student_model = "qwen-plus"
teacher_model = "qwen-long"


# 基类
class Character:

    def __init__(
        self, agent: Agent, identity: str, forget_ratio: float, permanent: int
    ):
        self.agent = agent
        self.identity = identity
        self.forget_ratio = forget_ratio
        self.permanent = permanent
        self.content_id = agent.name + "_m.json"
        logger.info(
            f"[{self.agent.name}][角色初始化] name:{agent.name}, forget_ratio:{forget_ratio}, permanent:{permanent}\n[Agent_instructions]:\n{agent.instructions}"
        )

    # 加载上下文
    def content_load(self) -> list:
        try:
            with open(content_dir + self.content_id, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    # 覆盖上下文
    def content_cover(self, content):
        with open(content_dir + self.content_id, "w", encoding="utf-8") as file:
            json.dump(content, file, indent=4, ensure_ascii=False)
            logger.debug(
                f"[{self.agent.name}][上下文记忆覆写] current_content = {content}"
            )

    # 随机遗忘上下文
    def forget(self):
        # 过滤参数
        if self.forget_ratio <= 0 or self.permanent <= 0:
            return

        logger.debug(f"[{self.agent.name}] 触发遗忘。")
        memory = self.content_load()
        if len(memory) == 0:
            return
        cnt = 0
        for msg in memory[::-1]:
            # 永久记忆门限
            if cnt > self.permanent:
                break
            # 系统设定不能遗忘
            if msg["role"] == "system":
                continue

            tokens = tokenizer.cut(msg["content"])
            for token in tokens:
                if (
                    token[1] not in ["g", "w", "x", ""]
                    and random.random() <= self.forget_ratio
                ):
                    token[0] = mask
            msg["content"] = "".join([token[0] for token in tokens])
            cnt += 1
        self.content_cover(content=memory)

    # 追加上下文，表现上等同于 remember
    def remember(self, msg):
        logger.debug(f"[{self.agent.name}][添加新上下文] new_msg:{msg}")
        memory = self.content_load()
        memory.append(msg)
        self.content_cover(content=memory)

    # 基础对话交互功能
    def talk(self, content: str) -> str:
        talk_id = str(uuid.uuid1())[:23]
        logger.info(
            f"[{self.agent.name}][对话][{talk_id}] 对话交互开始\nQuestion:\n{content}"
        )
        self.remember({"role": "user", "content": content})
        memory = self.content_load()
        try:
            rsp = client.run(agent=self.agent, messages=memory)
            answer = rsp.messages[-1]["content"]
            # 这里加入强制 format 输出
            answer = lab.format(id=self.identity, name=self.agent.name, content=answer)
            logger.info(
                f"[{self.agent.name}][对话][{talk_id}] 对话交互结果\nAnswer:\n{answer}"
            )
            self.remember({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            logger.error(f"[Character]对[{self.agent.name}]执行 talk 方法出现异常!")
            logger.exception(e)
            return f"[{self.identity}][{self.agent.name}]抱歉，这个问题我无法回答。"


# 学生
class Student(Character):

    def __init__(
        self, name: str, forget_ratio: float = 0.1, permanent: int = 75, extra_description=""
    ):
        new_agent = Agent(
            name=name,
            model=student_model,
            instructions=f"你的身份是一名学生，姓名是{name}。{extra_description}\n"
            + "你的任务事在接下来的一段时间里，你需要完成对特定的课程的学习。"
            + "具体目标如下：\n"
            + "- **主要目标**：在接下来的一段时间内学习特定课程的内容，顺利通过考试，并在学期结束时的期末测试中取得优异的成绩。"
            + "- **重要**：在老师授课过程中应当做好知识总结，禁止在老师授课过程中频繁提问，扰乱课堂节奏。"
            + "- **建议**：课程中，如果有疑问可以先记录整理，课堂最后会安排专门的老师答疑时间。答疑时间内可以单独向老师提问请教，寻求帮助。"
            + "- **重要**：禁止频繁提问，禁止提问时间过长，避免占用老师太多的时间。"
            + "- **建议**：课后时间，你可以与同学交流学习，巩固知识，但注意，课后时间有限，禁止交流时间太长，不要询问过于简单和基础的问题浪费老师的时间。"
            + "\n"
            + "在执行上述任务时，请你使用以下功能："
            + "1. 如果需要班级所有学生的名单，使用 `aware_roster` 函数。"
            + "2. 如果需要和班级中的某个学生进行一对一交流，要求先使用 `aware_roster` 函数获取班级中学生的名单，再使用 `talk2` 函数和名单中的同学进行交流。"
            + "3. 如果需要询问老师问题，或与老师进行一对一交流，使用 `ask_teacher` 函数。"
            + extra_prompt,
            functions=[talk2, aware_roster, ask_teacher],
        )
        super().__init__(
            agent=new_agent,
            forget_ratio=forget_ratio,
            permanent=permanent,
            identity="学生",
        )
        # 学生加入花名册
        roster[name] = self


# 老师
class Teacher(Character):

    def __init__(self, name: str):
        new_agent = Agent(
            name=name,
            model=teacher_model,
            # TODO
            instructions=f"你的身份是一名老师，姓名是{name}。"
            + "你的工作是负责按照教学安排和要求进行授课，确保你的学生理解和掌握课程内容。"
            + "具体任务如下："
            + "- **主要目标**：根据课程大纲和教学任务计划，进行授课和完成教学任务"
            + "- **要求**：根据课时安排和教学材料设计课程计划和教学大纲，然后根据教学计划和教学大纲进行教学。"
            + "- **要求**：进行教学任务时，如果涉及到教材相关的内容，要求你自己根据教材的内容，将教材中的知识提取总结后，再教授给同学们。"
            + "- **建议**：根据学生的学习情况，你可以组织课堂讨论，项目分析，案例探究等教学活动，以评估学生的学习成果。"
            + "- **要求**：如果需要对学生进行活动安排，要求必须先知道班级学生的名单。"
            + "\n"
            + extra_prompt
            + "在执行上述任务时，请你使用以下功能："
            + "1. 如果需要班级所有学生的名单，使用 `aware_roster` 函数。"
            + "2. 如果需要和班级中的某个学生进行一对一交流，要求先使用 `aware_roster` 函数获取班级中学生的名单，再使用 `talk2` 函数和名单中的同学进行交流。"
            + "3. 完成教学任务的过程中，需要对全班同学传授知识，讲课，组织课堂讨论，安排测试时，要求使用 `broadcast` 函数。",
            functions=[talk2, aware_roster, broadcast],
        )
        super().__init__(agent=new_agent, forget_ratio=0, permanent=0, identity="老师")
        # 老师加入 list
        teacher_list.append(self)

    def add_textbook(self, id: str):
        self.remember({"role": "system", "content": f"fileid://{id}"})
        return


# functions[]
# 和其他学生交流的能力
def talk2(name: str, content: str) -> str:
    """
    用于主动发起和班级里的其他学生交流，班级学生名单只允许通过 aware_roster 函数获取。

    参数:
    name(str): 想要交谈的学生的名字，班级学生名单只允许通过 aware_roster 函数获取。
    content(str): 想要交谈的内容，严格要求开头携带“[身份][姓名]”形式的前缀，表明身份和姓名。。

    返回值:
    str: 对方的回答。
    """

    student_recv = roster.get(name)
    if student_recv == None:
        logger.error(f"[Function][talk2]所在的班级没有这个人！期望交流内容\n{content}")
        return "名字出错了，没有找到这个人，请先获取班级里学生的名单再交流。"

    # 对调用方 assistant 的 content 添加记忆
    id, orignal = get_id_name(content=content)
    logger.debug(
        f"[Function][talk2] 函数被调用，调用发起方[{id}][{orignal}]，被调用方[{name}]"
    )
    if id == "学生":
        roster[orignal].remember({"role": "assistant", "content": content})
    elif id == "老师":
        teacher_list[0].remember({"role": "assistant", "content": content})

    # 直接交流（对方自己会持久化记忆）
    lab.conversation(id="学生", to=name, msg=content)
    ans = student_recv.talk(content)
    lab.conversation(id=id, to=orignal, msg=ans)

    # 对调用方 assistant 的 content 添加记忆（对面的回答相当于 user）
    if id == "学生":
        roster[orignal].remember({"role": "user", "content": ans})
    elif id == "老师":
        teacher_list[0].remember({"role": "user", "content": ans})

    return ans


# 感知班级环境的能力：获取学生花名册
def aware_roster() -> list:
    """
    用于拿到班级所有学生的名单。

    返回值:
    list: 班级所有学生姓名的列表
    """

    return list(roster.keys())


# 学生和老师交流的方法
def ask_teacher(content: str) -> str:
    """
    用于和老师交流。

    参数:
    content(str): 你想要交流对话的内容。强制要求开头携带“[身份][姓名]”形式的前缀，表明身份和姓名。所有数学公式都使用 LaTeX 格式。如果需要独立的公式块，请使用 `$$` 包裹，如果需要行内公式，请使用 `$` 包裹。

    返回值:
    str: 对方的回应。
    """

    if teacher_list == []:
        logger.error(
            f"[Function][ask_teacher]所在的班级没有老师！期望交流内容\n{content}"
        )
        return "你所在的班级没有老师。"

    # 对调用方 assistant 的 content 添加记忆
    id, orignal = get_id_name(content=content)
    logger.debug(f"[Function][ask_teacher] 函数被调用，调用方[{id}][{orignal}]。")
    if id == "学生":
        roster[orignal].remember({"role": "assistant", "content": content})

    # 调用 talk 和对方交流（对方自己会持久化记忆）
    lab.conversation(id="教师", to=teacher_list[0].agent.name, msg=content)
    ans = teacher_list[0].talk(content)
    lab.conversation(id=id, to=orignal, msg=ans)

    # 对调用方 assistant 的 content 添加记忆（对面的回答相当于 user）
    if id == "学生":
        roster[orignal].remember({"role": "user", "content": ans})
    return ans


# 对学生广播
def broadcast(content: str) -> dict:
    """
    用于老师同时对全班同学进行交流的函数，交流的内容会同时传达给所有学生，并获取学生的反馈。

    参数:
    content(str)：老师这次交流内容。强制要求开头携带“[身份][姓名]”形式的前缀，表明身份和姓名。所有数学公式都使用 LaTeX 格式。如果需要独立的公式块，请使用 `$$` 包裹，如果需要行内公式，请使用 `$` 包裹。

    返回值:
    dict: 所有学生对次交流的回答或反馈，key 是学生名字，value 是学生的回答或反馈。
    """
    feedback = dict()
    logger.debug(f"[Function][broadcast] 函数被调用:\n{content}")
    id, origin = get_id_name(content=content)
    if id == "老师":
        teacher_list[0].remember({"role": "assistant", "content": content})

    # 依次调用 talk 函数，达成广播
    lab.broadcastQ(id=id, origin=origin, msg=content)
    for k, v in roster.items():
        ans = v.talk(content)
        if id == "老师":
            teacher_list[0].remember({"role": "user", "content": ans})
        feedback[k] = ans
    lab.broadcastA(id=id, to=origin, msgs=list(feedback.values()))
    return feedback


# tool
# 让所有学生进行遗忘
def all_forget():
    logger.debug(f"[Tool_Function][all_forget] 函数被调用")
    for name, student in roster.items():
        student.forget()
        logger.debug(f"[Tool_Function][all_forget] {name}完成一轮次遗忘")
    logger.debug(f"[Tool_Function][all_forget] 所有学生完成一轮次遗忘")


# 让特定学生进行遗忘
def let_forget(name):
    logger.debug(f"[Tool_Function][let_forget] 函数被调用")
    if roster[name]:
        roster[name].forget()
        logger.debug(f"[Tool_Function][let_forget] {name}完成一轮次遗忘")
    else:
        logger.warning(f"[Tool_Function][let_forget] 没有找到{name}")
