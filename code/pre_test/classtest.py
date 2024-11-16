from pre_cfg import *
from character import Student,Teacher

t = Teacher("张老师",0.1,10)

s1 = Student("张三",0.1,10)
s2 = Student("李四",0.1,10)

perfix = "[管理员][Dawn]"
ans = t.talk("[管理员][Dawn]今天的课堂问题是“你对AI智能体的发展有什么看法”，你要收集学生的回答，并作出评价，然后将全部内容整理好交给我")
logger.info(f"[Answer]:{ans}")