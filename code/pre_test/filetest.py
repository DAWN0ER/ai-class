from domain.pre_cfg import logger,open_ai_client
from domain.aifile import Manager
import json

# from domain.character import Teacher

# file_obj = open_ai_client.files.create(file=Path("./lab/故乡.txt"), purpose="file-extract")
# logger.info(f"[File]{file_obj.model_dump_json}")
# file_id = file_obj.id
# ai = Teacher("周老师")
# ai.add_textbook(id=file_id)

# ai.talk("[校长][杨傲天]请告诉我这本小说讲了什么故事")

# master = Manager(cfg_path='./lab/file_cofig.json')

# ls =  open_ai_client.files.list()
# logger.info(f"文件列表\n{ls.to_json()}")
# l = master.list_file()
# logger.info(f"本地列表:{l}.")
# master.flush_file('./lab/故乡.txt')
# ls =  open_ai_client.files.list()
# logger.info(f"文件列表\n{ls.to_json()}")
# l = master.list_file()
# logger.info(f"本地列表:{l}.")

files = Manager(cfg_path='./lab/file_cofig.json')
ls = files.list_file()
for i in ls:
    logger.info(f"Type:{type(i)}, name={i.name},id={i.id},path={i.path},md5={i.md5}")
file = files.get_file(ls[0].path)
logger.info(f"Type:{type(file)}, name={file.name},id={file.id},path={file.path},md5={file.md5}")