import cmd
from domain.character import talk2,broadcast,aware_roster,ask_teacher

class InterCmd(cmd.Cmd):

    prompt = '[校长][杨校长]'

    def do_quit(self, arg):
        """Exit the command loop."""
        print(">>>交互结束<<<")
        return True 

    def do_student(self, arg):
        name, content = map(str, arg.split())
        print(f"name={name}, content={content}")
        ans = talk2(name=name,content=self.prompt+content)
        print(f">>>Result<<<\n{ans}")
    

    def do_roster(self, arg):
        print(f">>>花名册<<<{aware_roster()}")

    def do_broadcast(self,arg):
        content = self.prompt+arg
        feedback = broadcast(content=content)
        print(f">>>>>大家的回应<<<<<")
        for k,v in feedback.items():
            print(f"姓名:{k}\n{v}")

    def do_teacher(self,arg):
        content = self.prompt+arg
        ans = ask_teacher(content=content)
        print(f">>>Result<<<\n{ans}")
