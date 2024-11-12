from swarm import Swarm, Agent
from openai import OpenAI
import json
import thulac
import random

'''
n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
v/动词 a/形容词 d/副词 h/前接成分 k/后接成分 
i/习语 j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
e/叹词 o/拟声词 g/语素 w/标点 x/其它 
'''

test = '''全名：超古代怪兽-哥尔赞，身高：62米，体重：6万8千吨。
哥尔赞与迪迦奥特曼战斗中被打败之后，遁入地底的哥尔赞潜入雾门岳山地底，积蓄火焰岩浆能量来强化自己，使自己变为强化型的哥尔赞。
强化后的哥尔赞具有比以前哥尔赞更强的实力。积蓄岩浆能量，战斗力提高的哥尔赞。头部有像盔甲一样的装甲、强韧的皮肤、尖锐的指甲、巨大的力量，配合威力强大的强化超音波光线攻击对手。
'''

tokenizer = thulac.thulac(
    seg_only = False,
    filt = False
)

forget_ratio = 0.1
mask = "█"
max_loop = 5

def remember_and_forget(new_thing, memory = []):
    if (memory == []):
        memory.append(new_thing)
        return memory
    for msg in memory:
        tokens = tokenizer.cut(msg["content"])
        for token in tokens:
            if(token[1] not in ["g","w","x",""] and random.random() <= forget_ratio):
                token[0] = mask
        msg["content"] = ''.join([token[0] for token in tokens])
    memory.append(new_thing)
    return memory



if __name__ == "__main__":
    test = [
        {"role":"user","content":"全名：超古代怪兽-哥尔赞，身高：62米，体重：6万8千吨。"},
        {"role":"user","content":"哥尔赞与迪迦奥特曼战斗中被打败之后，遁入地底的哥尔赞潜入雾门岳山地底，积蓄火焰岩浆能量来强化自己，使自己变为强化型的哥尔赞。"},
        {"role":"user","content":"强化后的哥尔赞具有比以前哥尔赞更强的实力。"},
        {"role":"user","content":"积蓄岩浆能量，战斗力提高的哥尔赞。头部有像盔甲一样的装甲、强韧的皮肤、尖锐的指甲、巨大的力量，配合威力强大的强化超音波光线攻击对手。"},
        {"role":"user","content":"这是无关信息。"},
        {"role":"user","content":"这是无关信息*2。"},
    ]
    memorys = []

    for msg in test:
        print(f"msg input = {msg['content']}")
        memorys = remember_and_forget(new_thing=msg,memory=memorys)
        ans = ''.join([memory['content']+'\n' for memory in memorys])
        print(f"memory: \n{ans}")