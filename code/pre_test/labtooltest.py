from domain.character import (
    Teacher,
    ask_teacher
)
from domain.labtools import create_json_script
from domain.aifile import Manager

# manager = Manager(cfg_path="./lab/file_cofig.json")
# TEXT_BOOK = "./lab/通信电路与系统教学资料.md"

Teacher("王武")

ask_teacher("[校长][徐清远]什么是麦克斯韦方程？")
create_json_script()
