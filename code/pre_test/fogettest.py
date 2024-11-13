from character import Student,Character
from swarm import Swarm,Agent
from openai import OpenAI
import sys

text = """怪兽-雷克戈涅杰厄，身高200米。体重200000吨，复活于南太平洋海底的古代遗迹露赛德露耶。
怪兽-雷克戈涅杰厄是露赛德露耶古代遗迹中复苏的邪神，3000万年前毁灭超古代文明的元凶，也是最终的黑暗，刚刚苏醒便召唤出无尽的黑暗直接覆盖了整个地球。
怪兽-雷克戈涅杰厄的菊石状的身体异常庞大，和战士-斯芬涅洛斯战斗时只露出了身体的上半部分，下身站在上浮的露赛德露耶遗迹上。
怪兽-雷克戈涅杰厄头部眼睛和嘴的位置与人类上下颠倒，全身都是坚硬的铠甲甲壳，战士-斯芬涅洛斯的任何光线都无法伤其分毫。
怪兽-雷克戈涅杰厄甲壳下长满无数的触手，双手是巨大的钳子，可以自由伸长从水下偷袭对手。
怪兽-雷克戈涅杰厄实力极强，常态战士-斯芬涅洛斯完全不是对手，仅仅几根触手的力量便能控制住强力型战士-斯芬涅洛斯。其触手可以吸取对手的能量。
怪兽-雷克戈涅杰厄口中能吐出带电的黑暗迷雾，这黑雾能轻易入侵TPC基地并瘫痪破坏其电子设备，无法用物理的力量阻挡，人类接触到就会瞬间死亡，战士-斯芬涅洛斯则被灼伤和消耗能量。
怪兽-雷克戈涅杰厄在战斗中接连接下了战士-斯芬涅洛斯的迪拉休姆光流和强化版哉佩利奥光线，但毫发无伤，随即一发贯穿光线直接抽光了战士-斯芬涅洛斯的能量，使其还原为石像状态，意识虽在但也无法变回人形。
战斗的最后关键时刻，全世界的孩子们变成光进入战士-斯芬涅洛斯体内，使其复活并升级为闪耀型战士-斯芬涅洛斯，以压倒性的优势击杀了怪兽-雷克戈涅杰厄。"""

api_key = open("./code/api_key.cfg").readline()

client = Swarm(
    client= OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
)

agent = Agent(
    name="知识助手",
    instructions="你是一个知识助手，接下来的对话会告诉你一系列你需要记住的知识点，其中被“█”代替的内容为未知的信息。学习知识时只需要回答“了解”就可以。然后会有提问，请你根据你记忆的知识点推理回答。",
    model="qwen-long"
)

s = Character(
    anget=agent,
    client=client,
    forget_ratio = 0.25,
    permanent=32
)

prefix = "下面是你这次需要学习的内容："

msglist = text.split("\n")
question = "问题：根据已经学习的内容，回答怪兽-雷克戈涅杰厄的身高，体重，外貌，战斗能力等基本信息。"

file = open('output5f.log','w')
sys.stdout = file

for idx,msg in enumerate(msglist) :
    print(f"=====第{idx+1}次对话=====")
    print(f"[知识]:{msg}")
    print(f"[Agent记忆]:{s.memory}")
    ans = s.talk(prefix+msg)
    print(f"[Agent回答]:{ans}")
    if (idx % 4 == 0):
        print(f"[测试问题]:{question}")
        print(f"[Agent记忆]:{s.memory}")
        ans = s.talk(question)
        print(f"[Agent回答]:{ans}")
    s.forget()

sys.stdout = sys.__stdout__
file.close()