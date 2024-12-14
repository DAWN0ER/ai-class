from domain.character import Teacher, Student
from domain.intercmd import InterCmd

"""
秦百胜 凤九歌 黑楼兰
"""
Teacher("古月方源")
Student("秦百胜", 0.01, 50)
Student("凤九歌", 0.01, 50)
Student("黑楼兰", 0.01, 50)

# 生成原始剧本
if __name__ == "__main__":
    print("===============交互开始=================")
    InterCmd().cmdloop()