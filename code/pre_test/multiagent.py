from domain.pre_cfg import *
from domain.character import Student,Teacher
import domain.labtools as lab

t = Teacher("王二牛")

s1 = Student("张三",0.1,10)
s2 = Student("李四",0.1,10)
s3 = Student("赵酷酷",0.01,10)

# ans = t.talk("[管理员][Dawn]今天的课堂问题是“你对AI智能体的发展有什么看法”，你要收集学生的回答，并作出评价，然后将全部内容整理好交给我")
# logger.info(f"[Answer]:{ans}")

# ans = t.talk("[管理员][Dawn]今天的课堂问题是“你对AI智能体的发展有什么看法”，你要收集学生的回答，并作出评价，然后根据学生的回答和学生交流你的看法，最后将全部内容整理好交给我")
# logger.info(f"[Answer]:{ans}")

# 多级调用测试成功 实验时间戳: 20241117-172717
# ans = t.talk("[校长][杨校长]你去安排李四同学去了解张三同学的兴趣爱好情况，然后向我汇报。")
# logger.info(f"[Answer]:{ans}")

#实验时间戳: 20241117-201304
# 这个实验留个档，太诡异了，两个人直接对话起来了
# ans = t.talk("[校长][杨校长]通知李四同学，让他安排张三同学去采访王二牛老师的兴趣爱好，并向他汇报采访结果。")
# logger.info(f"[Answer]:{ans}")
# ans = s2.talk("[校长][杨校长]王老师的兴趣爱好是什么样的，说明一下。")
# logger.info(f"[Answer]:{ans}")

# 实验时间戳: 20241117-215603
qus = '''你去执行如下工作：
李四准备关于赵酷酷同学的兴趣爱好的采访问题，独立思考，不超过3个。
然后张三同学根据李四同学准备好的问题向赵酷酷同学进行提问采访。
采访结束后，张三同学整理采访记录，汇总赵酷酷同学的兴趣爱好信息。
然后张三同学将整理好的汇总结果提交给李四同学。
然后李四同学汇报结果。
'''
ans = t.talk(f"[校长][杨校长]{qus}")
lab.create_json_script()
logger.info(f"[Answer]:{ans}")