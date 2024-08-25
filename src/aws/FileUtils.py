import os
import s3fs

# AWS Access Token
aws_id = os.environ['AWS_ID']
aws_secret = os.environ['AWS_SECRET']
bucket = 'galactickittenss'
s3 = s3fs.S3FileSystem(key=aws_id, secret=aws_secret)

def ListDirectory(directory : str) -> list[str]:
    directory = f'{bucket}/blog/{directory}/'
    objs : list[str] = s3.listdir(directory, detail=False)
    return [file.replace(directory, '') for file in objs if file != directory]

def Exists(filename : str) -> bool:
    return s3.exists(f'{bucket}/blog/{filename}')

def ReadBytes(filename : str) -> bytes:
    with s3.open(f'galactickittenss/blog/{filename}', 'rb') as f:
        return f.read()

def Read(filename : str) -> str:
    return ReadBytes(filename).decode()

def Remove(filename : str):
    print("Using FileUtils.Remove, which is currently broken.")

def SaveString(filename : str, contents : str):
    print("Using FileUtils.SaveString, which is currently broken.")
