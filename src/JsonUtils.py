import json

def GetString(file : dict, name : str, default : str = '') -> str:
    if file.get(name) is not None:
        return file[name]
    return default

def GetBool(file : dict, name : str, default : bool = False) -> bool:
    if file.get(name) is not None:
        return file[name]
    return default

def GetList(file : dict, name : str) -> list[dict]:
    if file.get(name) is not None:
        return file[name]
    return []

def LoadFromPath(path: str) -> dict:
    with open(path, 'r') as f:
        file = json.load(f)

    return file

def SaveToPath(obj : dict, path : str) -> None:
    with open(path, 'w') as f:
        json.dump(obj, f, indent=4)