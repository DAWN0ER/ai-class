import cmd
from domain.pre_cfg import logger
from domain.character import (
    talk2,
    broadcast,
    aware_roster,
    ask_teacher,
    all_forget,
    let_forget,
)
import domain.labtools as lab


class InterCmd(cmd.Cmd):

    prompt = "[校长][杨校长]"

    def do_quit(self, arg):
        """Exit the command loop."""
        logger.info("[quit]交互结束")
        # 生成 replay 剧本
        lab.create_json_script()
        print(">>>交互结束<<<")
        return True

    def do_student(self, arg):
        """talk to Student [name] [content]"""
        logger.info(f"[studnet]:{arg}")
        name, content = map(str, arg.split())
        print(f"name={name}, content={content}")
        ans = talk2(name=name, content=self.prompt + content)
        print(f">>>Result<<<\n{ans}")

    def do_roster(self, arg):
        print(f">>>花名册<<<{aware_roster()}")

    def do_broadcast(self, arg):
        logger.info(f"[broadcast]:{arg}")
        content = self.prompt + arg
        feedback = broadcast(content=content)
        print(f">>>>>大家的回应<<<<<")
        for k, v in feedback.items():
            print(f"姓名:{k}\n{v}")

    def do_teacher(self, arg):
        logger.info(f"[teacher]:{arg}")
        content = self.prompt + arg
        ans = ask_teacher(content=content)
        print(f">>>Result<<<\n{ans}")

    def do_forget(self, arg):
        logger.info(f"[forget]{arg}学生开始模拟遗忘")
        if arg == "ALL":
            all_forget()
        else:
            let_forget(name=arg)
        print(">>>遗忘完成<<<")
