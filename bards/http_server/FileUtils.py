import os
import glob

def ListDirectory(directory : str) -> list[str]:
    return os.listdir(directory)

def GetFilesRecursively(directory : str) -> list[str]:
    directory += "\\"
    objs = glob.iglob(directory + "**/**", recursive=True)
    objs = list(dict.fromkeys(objs)) # Remove Duplicates
    return [file.replace(directory, '') for file in objs if not os.path.isdir(file)]


def Exists(filename : str) -> bool:
    return os.path.exists(filename)

def ReadBytes(filename : str) -> bytes:
    with open(filename, 'rb') as f:
        return f.read()

def Read(filename : str) -> str:
    return ReadBytes(filename).decode()

def Remove(filename : str):
    os.remove(filename)

def SaveString(filename : str, contents : str):
    with open(filename, 'w') as f:
        f.write(contents)