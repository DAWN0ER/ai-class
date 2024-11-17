from pre_cfg import *
from character import Student,Teacher

t = Teacher("张老师")

s1 = Student("张三",0.1,10)
s2 = Student("李四",0.1,10)

# ans = t.talk("[管理员][Dawn]今天的课堂问题是“你对AI智能体的发展有什么看法”，你要收集学生的回答，并作出评价，然后将全部内容整理好交给我")
# logger.info(f"[Answer]:{ans}")

# ans = t.talk("[管理员][Dawn]今天的课堂问题是“你对AI智能体的发展有什么看法”，你要收集学生的回答，并作出评价，然后根据学生的回答和学生交流你的看法，最后将全部内容整理好交给我")
# logger.info(f"[Answer]:{ans}")

ans = t.talk("[校长][杨校长]你去安排李四同学去了解张三同学的兴趣爱好情况，然后向我汇报。")
logger.info(f"[Answer]:{ans}")