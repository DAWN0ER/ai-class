from domain.pre_cfg import log_dir, logger, time_format
import json, re, random, copy

# 原始剧本文件位置
SCRIPT_TXT = log_dir + "script.txt"
SCRIPT_JSON = f"./web/cache/{time_format}-script.json"

# 剧本生成常量
pattern = r"^\[(.*?)\]\[(.*?)\]"
stack = []
sceneList = []
sceneOrderNow = 0

sImgs = ["boy_" + str(i + 1) for i in range(8)] + [
    "girl_" + str(i + 1) for i in range(8)
]
random.shuffle(sImgs)
sNames = []
tImgs = ["teacher_" + str(i + 1) for i in range(4)]
random.shuffle(tImgs)
tNames = []


def __append_line(
    type: str,
    msgs: list,
    info: dict,
):
    newline = json.dumps({"type": type, "info": info, "msg": msgs}, ensure_ascii=False)
    logger.debug(f"[Script] Append:{newline}")
    try:
        with open(SCRIPT_TXT, "a", encoding='utf-8') as file:
            file.write(newline + "\n")
    except Exception as e:
        logger.error(f"[Script] Error with line: {newline}")
        logger.exception(e)


def broadcastQ(id: str, origin: str, msg: str):
    info = {"id": id, "from": origin}
    __append_line(type="broadcast", info=info, msgs=[msg])


def broadcastA(id: str, to: str, msgs: list):
    info = {"id": id, "to": to}
    __append_line(type="broadcast", info=info, msgs=msgs)


def conversation(id: str, to: str, msg: str):
    info = {"id": id, "to": to}
    __append_line(type="conversation", info=info, msgs=[msg])
    return


# 强制 format 的二代保险
def format(id: str, name: str, content: str):
    match = re.match(pattern=pattern, string=content)
    if match:
        return content
    return f"[{id}][{name}]{content}"


# 剧本生成相关操作


def __match_pattern(content: str):
    match = re.match(pattern=pattern, string=content)
    if match:
        id = match.group(1)
        name = match.group(2)
        return id, name, content.removeprefix(f"[{id}][{name}]")
    else:
        logger.warning(f"[SCRIPT] 解析正则表达式失败：{content}")
        return "未知身份", "匿名", content


def __get_img(name: str, id: str):
    names = sNames if id == "学生" else tNames
    imgs = sImgs if id == "学生" else tImgs
    if name not in names:
        names.append(name)
    return imgs[names.index(name)]


def __change_to_scene(data, scriptId):
    # 基本信息
    nextScene = {"script": scriptId}
    nextScene["order"] = sceneOrderNow + 1
    nextScene["scene"] = data["type"]

    # 剧本具体人物互动信息
    if data["type"] == "conversation":
        idL, nameL, msgL = __match_pattern(data["msg"][0])  # from
        nameR = data["info"]["to"]
        idR = data["info"]["id"]
        nextScene["talkerL"] = {  # from
            "name": nameL,
            "id": idL,
            "img": __get_img(name=nameL, id=idL),
            "msg": msgL,
        }
        nextScene["talkerR"] = {  # to
            "name": nameR,
            "id": idR,
            "img": __get_img(name=nameR, id=idR),
            "msg": "",
        }
    elif data["type"] == "broadcast":
        info = data["info"]
        if "from" in info:  # 发起
            id, name, msg = __match_pattern(data["msg"][0])  # from
            nextScene["speaker"] = {
                "name": name,
                "id": id,
                "img": __get_img(name=name, id=id),
                "msg": msg,
            }
            nextScene["students"] = []
        elif "to" in info:
            nextScene["speaker"] = {
                "name": info["to"],
                "id": info["id"],
                "img": __get_img(name=info["to"], id=info["id"]),
                "msg": "",
            }
            students = []
            for aMsg in data["msg"]:
                sid, sname, message = __match_pattern(aMsg)
                students.append(
                    {
                        "name": sname,
                        "msg": message,
                        "img": __get_img(name=sname, id=sid),
                    }
                )
            nextScene["students"] = students
    return nextScene


def __is_match(nowData):
    if len(stack) < 1:
        return False
    sceneData = stack[-1]
    if sceneData["scene"] != nowData["scene"]:
        return False
    if nowData["scene"] == "conversation":
        return (
            nowData["talkerL"]["name"] == sceneData["talkerR"]["name"]
            and nowData["talkerR"]["name"] == sceneData["talkerL"]["name"]
        )
    elif nowData["scene"] == "broadcast":
        return nowData["speaker"]["name"] == sceneData["speaker"]["name"]
    return False


# 默认是匹配的
def merge_scene(oldScene, newScene, order):
    if newScene["scene"] == "conversation":
        oldScene["order"] = order
        oldScene["talkerR"]["msg"] = newScene["talkerL"]["msg"]
        return oldScene
    if newScene["scene"] == "broadcast":
        oldScene["order"] = order
        oldScene["students"] = newScene["students"]
        return oldScene


def create_json_script(scriptId=time_format):
    # 初始化参数
    global sceneOrderNow
    stack.clear()
    sceneList.clear()
    sceneOrderNow *= 0
    sNames.clear()
    tNames.clear()
    if scriptId == time_format:
        original_script = SCRIPT_TXT
        output_script = SCRIPT_JSON
    else:
        original_script = f"./logs/{scriptId}/script.txt"
        output_script = f"./web/cache/{scriptId}-script.json"

    # 读取原始剧本
    with open(original_script, "r", encoding='utf-8') as file:
        while True:
            line = file.readline().rstrip("\n")
            if line == "":
                break
            data = json.loads(line)
            nextScene = __change_to_scene(data=data, scriptId=time_format)
            if not __is_match(nextScene):
                sceneOrderNow += 1  # 和最新的 scenelist 里的最新的 scene 的 order 对齐
                stack.append(nextScene)
                sceneList.append(copy.deepcopy(nextScene))
                continue

            # 如果正好和上一个场景匹配，就直接加入上一个场景，否者就整合成新场景
            useOrder = nextScene["order"]
            if len(stack) > 0 and stack[-1]["order"] == sceneOrderNow:
                useOrder = sceneOrderNow
                sceneList.pop()
            oldOne = stack.pop()
            mergeScene = merge_scene(
                oldScene=oldOne, newScene=nextScene, order=useOrder
            )
            sceneOrderNow = mergeScene["order"]
            sceneList.append(copy.deepcopy(mergeScene))
    logger.debug(f"stack:{stack}")
    with open(file=output_script, mode="w", encoding='utf-8') as fp:
        json.dump(obj=sceneList, fp=fp, ensure_ascii=False, indent=4)
