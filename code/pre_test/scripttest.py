import json, re, random, copy

SCRIPT_ID = "20241214-190250"
file_path = f"./logs/{SCRIPT_ID}/script.txt"
output_path = f"./lab/{SCRIPT_ID}.json"
pattern = r"^\[(.*?)\]\[(.*?)\](.*)"
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


def match_pattern(content: str):
    match = re.match(pattern=pattern, string=content)
    if match:
        return match.group(1), match.group(2), match.group(3)
    else:
        return "未知身份", "匿名", content


def get_img(name: str, id: str):
    names = sNames if id == "学生" else tNames
    imgs = sImgs if id == "学生" else tImgs

    if name not in names:
        names.append(name)
    # print(f"DEBUG: name = {name},idx={names.index(name)},id={id}")
    return imgs[names.index(name)]


def change_to_scene(data, scriptId):
    # 基本信息
    nextScene = {"script": scriptId}
    nextScene["order"] = sceneOrderNow + 1
    nextScene["scene"] = data["type"]

    # 剧本具体人物互动信息
    if data["type"] == "conversation":
        idL, nameL, msgL = match_pattern(data["msg"][0])  # from
        nameR = data["info"]["to"]
        idR = data["info"]["id"]
        nextScene["talkerL"] = {  # from
            "name": nameL,
            "id": idL,
            "img": get_img(name=nameL, id=idL),
            "msg": msgL,
        }
        nextScene["talkerR"] = {  # to
            "name": nameR,
            "id": idR,
            "img": get_img(name=nameR, id=idR),
            "msg": "",
        }
    elif data["type"] == "broadcast":
        info = data["info"]
        if "from" in info:  # 发起
            id, name, msg = match_pattern(data["msg"][0])  # from
            nextScene["speaker"] = {
                "name": name,
                "id": id,
                "img": get_img(name=name, id=id),
                "msg": msg,
            }
            nextScene["students"] = []
        elif "to" in info:
            nextScene["speaker"] = {
                "name": info["to"],
                "id": info["id"],
                "img": get_img(name=info["to"], id=info["id"]),
                "msg": "",
            }
            students = []
            for aMsg in data["msg"]:
                sid, sname, message = match_pattern(aMsg)
                students.append(
                    {"name": sname, "msg": message, "img": get_img(name=sname, id=sid)}
                )
            nextScene["students"] = students
    return nextScene


def is_match(nowData):
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


with open(file_path, "r") as file:
    while True:
        line = file.readline().rstrip("\n")
        if line == "":
            break
        data = json.loads(line)
        nextScene = change_to_scene(data=data, scriptId=SCRIPT_ID)
        if not is_match(nextScene):
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
        mergeScene = merge_scene(oldScene=oldOne, newScene=nextScene, order=useOrder)
        sceneOrderNow = mergeScene["order"]
        sceneList.append(copy.deepcopy(mergeScene))

print(stack)
with open(file=output_path, mode="w") as fp:
    json.dump(obj=sceneList, fp=fp, ensure_ascii=False, indent=4)
