import json
from datetime import datetime

from Platform import FileUtils

def GetString(file : dict, name : str, default : str = '') -> str:
    if file.get(name) is not None:
        return file[name]
    return default

def GetBool(file : dict, name : str, default : bool = False) -> bool:
    if file.get(name) is not None:
        return file[name]
    return default

def GetDate(file : dict, name : str, format : str, default : datetime) -> datetime:
    if file.get(name) is not None:
        return datetime.strptime(file[name], format)
    return default

def GetList(file : dict, name : str) -> list[dict]:
    if file.get(name) is not None:
        return file[name]
    return []

def LoadFromPath(path: str) -> dict:
    file = FileUtils.Read(path)
    return json.loads(file)

def SaveToPath(obj : dict, path : str) -> None:
    FileUtils.SaveString(path, json.dumps(obj, indent=4))
