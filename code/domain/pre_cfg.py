from swarm import Swarm
from openai import OpenAI
from loguru import logger
import thulac,datetime,os,re,sys

time_format = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# 日志框架
log_dir = f"./logs/{time_format}/"
logger.remove(0) # 删除默认日志处理器
log_format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> <lc>|</lc> <level>{level}</level> <lc>|</lc> {message}"
logger.add(sys.stderr, level="INFO",format=log_format,colorize=True,)
logger.add(log_dir+"debug.log",level="DEBUG",format=log_format)
logger.add(log_dir+"app.log",level="INFO",format=log_format)

# 文件静态内容
my_model = "qwen-long"
mask = "█"

# 上下文持久化位置
content_dir = f"./logs/{time_format}/content/"
os.makedirs(content_dir, exist_ok=True)

# AI client
open_ai_client= OpenAI(
        api_key = open("./lab/api_key.cfg").readline(),
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
client = Swarm(
    open_ai_client
)

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