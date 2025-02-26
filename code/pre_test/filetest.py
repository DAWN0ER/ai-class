from domain.pre_cfg import logger, open_ai_client
from domain.aifile import Manager
from domain.character import Teacher

files = Manager(cfg_path="./lab/file_cofig.json")
ai = Teacher("周老师")

TEXT_BOOK = "./lab/通信电路与系统教学资料.md"
files.flush_file(TEXT_BOOK)

ai.add_textbook(files.get_file(TEXT_BOOK).id)
ans = ai.talk("[校长][杨傲天]总结《通信电路与系统教学资料》,这个资料有几个章节？，每个章节的内容是什么？")
print(ans)