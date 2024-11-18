from domain.pre_cfg import *
from pathlib import Path
import json,hashlib,os

class FileInfo:
    def __init__(self,name,path,md5,id):
        self.name = name
        self.path = path
        self.md5 = md5
        self.id = id
        pass

class Manager:
    def __init__(self,cfg_path:str):
        self.cfg_path = cfg_path
        cfg = []
        self.__sheet = dict()
        with open(cfg_path,'r',encoding='utf-8') as cfg_file:
            cfg = json.load(fp=cfg_file)
        for file in cfg:
            if self.check_md5(file):
                logger.info(f"[文件管理] 载入文件{file['path']}")
                self.__sheet[file['path']] = file
        pass
    
    def __update_cofig(self):
        with open(self.cfg_path,"w",encoding='utf-8') as cfg_file:
            cfg = list(self.__sheet.values())
            json.dump(cfg,cfg_file,indent=4,ensure_ascii=False)

    def list_file(self) -> list:
        return [FileInfo(**item) for item in self.__sheet.values()]

    def get_file(self, path:str) -> FileInfo:
        if path in self.__sheet:
            return FileInfo(**self.__sheet[path])
        return None
    
    def flush_file(self,path:str):
        if path in self.__sheet :
            file = self.get_file(path)
            if self.check_md5(file):
                logger.warning(f"MD5校验认定文件{path}未更改，不更新。")
                return
            self.del_file(path=path)
        file = dict()
        file['name'] = os.path.basename(path)
        file['path'] = path
        file['md5'] = self.file_md5(path)
        file_obj = open_ai_client.files.create(
            file=Path(path), purpose="file-extract"
            )
        logger.info(f"文件api请求结果:{file_obj.model_dump_json()}")
        file['id'] = file_obj.id
        logger.info(f"添加新文件:{file}")
        self.__sheet[path] = file
        self.__update_cofig()
    
    def del_file(self,path:str):
        if path in self.__sheet:
            file = self.get_file(path)
            try:
                file_del = open_ai_client.files.delete(file_id=file['id'])
                logger.info(f"删除旧文件:{file},rsp={file_del}")
            except Exception as e:
                logger.warning(f"删除失败:{file}",e)
            del self.__sheet[path]
            self.__update_cofig()

    def check_md5(self,file:dict):
        md5_record = file['md5']
        file_path = file['path']
        try:            
            md5_check = self.file_md5(file_path)
            return md5_record == md5_check
        except IOError as e:
            logger.exception(f"文件读取异常{file_path}",e)    
            return False

    ## 允许抛出异常
    def file_md5(self,file_path:str) -> str:
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:  # 以二进制读取模式打开文件
            for chunk in iter(lambda: f.read(4096), b''):  # 每次读取4096字节
                md5.update(chunk)
        return md5.hexdigest()
            