from fastapi import FastAPI

app = FastAPI()

# ? 뒤에 name=이름 으로 요청하는 형태를 쿼리형태라고 부른다.
@app.get("/items/name")
def read_name(name:str): # fast api에서는 hint를 통해 사용자에게 올바른 사용법을 유도한다.
    return {'name':name,'salary':10000000}

# 경로에 붙여들어오는 것을 경로형태 라고 부른다.
# items/id/123456789
@app.get("/items/id/{item_id}") # path variable
def read_id(item_id:int):
    return {'item_id':item_id}

# /download/sample.txt 는 가능하지만...
# folder/sample.txt 이 경우 /download/folder/{file_path} 로 인식하여 404가 나타난다.
@app.get("/download/{file_path:path}")
def download_file(file_path:str):
    return {'download_file':file_path}

# /download/sample.txt 로 들어오면...
# @app.get('/download/{file_path}') 이 요청을 찾는다.

# /download/folder/sample.txt 로 들어오면...
# @app.get('/download/folder/{file_path}') 이 요청을 찾는다.
