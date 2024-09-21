import os
import s3fs

# AWS Access Token
aws_id = os.environ['AWS_ID']
aws_secret = os.environ['AWS_SECRET']
bucket = os.environ['AWS_BUCKET']
s3 = s3fs.S3FileSystem(key=aws_id, secret=aws_secret)

def ListDirectory(directory : str) -> list[str]:
    directory = f'{bucket}/{directory}/'
    objs : list[dict[str, str]] = s3.listdir(directory, detail=True)
    return [file['Key'].replace(directory, '') for file in objs if file['type'] == 'file']

def GetFilesRecursively(directory : str) -> list[str]:
    directory = f'{bucket}/{directory}/'
    objs = s3.find(directory, detail=False)
    return [file.replace(directory, '') for file in objs]

def Exists(filename : str) -> bool:
    return s3.exists(f'{bucket}/{filename}')

def ReadBytes(filename : str) -> bytes:
    print(f"Opening '{bucket}/{filename}'")
    with s3.open(f'{bucket}/{filename}', 'rb') as f:
        return f.read() # type: ignore

def Read(filename : str) -> str:
    return ReadBytes(filename).decode()

def Remove(filename : str):
    print("Using FileUtils.Remove, which is currently broken.")

def SaveString(filename : str, contents : str):
    print("Using FileUtils.SaveString, which is currently broken.")
