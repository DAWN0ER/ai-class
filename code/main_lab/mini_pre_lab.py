from domain.character import Teacher, Student
from domain.aifile import Manager
from domain.intercmd import InterCmd

"""
林子涵 徐欣怡 李泽明 吴悠远 钱程远 陈思思
"""

manager = Manager(cfg_path="./lab/file_cofig.json")
teacher = Teacher("李天名")
teacher.add_textbook(manager.get_file("./lab/深度学习.pdf").id)
teacher.add_textbook(manager.get_file("./lab/故乡.txt").id)
Student("林子涵", 0.1, 50)
Student("徐欣怡", 0.1, 50)
Student("李泽明", 0.1, 50)
Student("吴悠远", 0.1, 50)
Student("钱程远", 0.1, 50)
Student("陈思思", 0.1, 50)

if __name__ == "__main__":
    print("===============交互开始=================")
    InterCmd().cmdloop()
