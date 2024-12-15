from domain.character import (
    Teacher,
    Student,
    ask_teacher,
    broadcast,
    # all_forget,
    # let_forget,
)
import domain.labtools as lab
from domain.aifile import Manager

teacher = Teacher("王建国")
Student("林子涵", 0.1, 50)
Student("徐欣怡", 0.1, 50)
Student("李泽明", 0.1, 50)
Student("吴悠远", 0.1, 50)
Student("钱程远", 0.1, 50)
Student("陈思思", 0.1, 50)
Student("周子轩", 0.1, 50)
Student("赵梓涵", 0.1, 50)
Student("孙悦心", 0.1, 50)
Student("郑宇轩", 0.1, 50)
Student("王梓萱", 0.1, 50)
Student("冯浩然", 0.1, 50)
Student("陈梦琪", 0.1, 50)

manager = Manager(cfg_path="./lab/file_cofig.json")
teacher.add_textbook(manager.get_file("./lab/故乡.txt").id)

prompt = "[校长][杨校长]"

# 流程 python -u ./code/main_lab/mini_loop_lab.py --log INFO
ans = ask_teacher(
    prompt
    + "现在进行教学任务安排：这个学期你是《中国近代文学赏析》这门课程的授课老师。"
    + "今天需要上第一节课，教学内容为赏析文章《故乡》，同学们手上并没有这篇文章的正文，需要你在教学过程中摘抄原文的关键内容教给同学们，才能让同学们了解学习的内容。"
    + "第一节课的教学要求如下：\n1. 了解这篇文章的基本内容，行文脉络。\n2. 解析小说中的人物情感变化。\n3.解析文章的思想主旨，学习作者想表达的感情。\n"
    + "现在，基于课程的教学内容，给出你的第一节课的教学计划。"
)
print(f">>>\n{ans}")

ans = ask_teacher(prompt + "给同学们介绍一下自己和课程安排。")
print(f">>>\n{ans}")

ans = broadcast(
    prompt
    + "同学们，现在正式开始上《中国近代文学赏析》的第一节课，本堂课的任课老师是王建国，请同学们安静，准备上课。"
)
print(f">>>\n{ans}")

ans = ask_teacher(
    prompt
    + "现在开始上第一节课，请按照你的教学计划，完成你第一节课的教学任务，完成教学任务后，总结这次的教学效果。"
)
print(f">>>\n{ans}")

ans = ask_teacher(
    prompt
    + "现在是教学活动安排时间，安排一次小组讨论，题目为“我记忆里的故乡”。"
)
print(f">>>\n{ans}")

ans = ask_teacher(
    prompt + "根据学生们的表现，总结一下这节课的教学质量，你觉得这次课怎么样怎么样。"
)
print(f">>>\n{ans}")

ans = broadcast(
    prompt
    + "现在是答疑时间，同学们如果有疑问可以向老师提问请教。注意不要占用太多时间。"
)
print(f">>>\n{ans}")

ans = broadcast(
    prompt
    + "现在下课，同学们自由安排，可以和同学相互交流，也可以自己整理复习这堂课的学习内容。"
)
print(f">>>\n{ans}")

ans = broadcast(prompt + "整理汇总《中国近代文学赏析》的第一节课的学习内容。")
print(f">>>\n{ans}")

lab.create_json_script()
