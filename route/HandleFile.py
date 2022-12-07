from fastapi.encoders import jsonable_encoder
import pandas as pd


class status:
    HTTP_404_NOT_FOUND = 404

class JSONResponse:
    def __init__(self,  result, Status, filename, content):
        self.result = result
        self.Status = Status
        self.filename = filename
        self.content = content


def saveFile(received_file, filename):
    with open(filename, 'wb') as f:
        f.write(received_file.read())


def readFile(filename):
    with open(filename, 'r') as f:
        content = f.read()
    print(content)
    return content

def catchData():
    file_raw = pd.read_json("./meida/data.json")
    file = file_raw['content']
    file.to_dict()
