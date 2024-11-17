from swarm import Swarm
from openai import OpenAI
import thulac
import datetime
from loguru import logger
import os
import re

time_format = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# 日志系统
log_dir = f"./logs/{time_format}/"
logger.add(log_dir+"app.log",level="INFO",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
logger.add(log_dir+"debug.log",level="DEBUG",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
logger.level = "INFO"
# 文件静态内容
my_model = "qwen-long"
mask = "█"
# 上下文持久化位置
content_dir = f"./logs/{time_format}/content/"
os.makedirs(content_dir, exist_ok=True)
# AI client
client = Swarm(
    client= OpenAI(
        api_key = open("./lab/api_key.cfg").readline(),
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
)
# 分词器
logger.info("[分词器] loading...")
tokenizer = thulac.thulac(
    seg_only = False,
    filt = False
)
logger.info("[分词器] completed...")

logger.info(
f'''实验静态参数配置：
实验时间戳: {time_format}
LLM模型: {my_model}
mask标记: {mask}
上下文持久化位置: {content_dir}
client base url: {client.client.base_url}'''
)

# tools

def get_id_name(content:str):
    pattern = r'^\[(.*?)\]\[(.*?)\]'
    match = re.match(pattern=pattern,string=content)
    if match:
        id = match.group(1)
        name = match.group(2)
        return id,name
    else:
        return '未知身份','匿名'