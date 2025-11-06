# 파일 업로드/다운로드를 위해 필요한 라이브러리
# pip install python-multipart
import os
import shutil
from typing import List

from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from logger import Logger

app = FastAPI()
logger = Logger().get_logger(__name__) # Logger 객체화
logger.info('log 준비완료!')

# 클라이언트로 부터 전송받음 -> 파일로 저장
FILE_PATH = './upload' # 전체 대문자 : 상수_변하지 않는 값
# 해당 경로가 존재하지 않으면 만들어라
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)

#CORS Policy
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])

# /images 라는 요청이 오면 서버내 파일이 저장된 폴더로 연결
# 이 경우 /images 라는 요청을 별도로 만들어 처리하기에 복잡하다.
# 그래서 요청과 폴더를 연결할 수 있는 기능을 제공한다.
# /images 라는 요청이 오면,
# 특정 경로로 연결(StaticFiles = 이미지,css,js 파일등 의미),
# 내부적으로 호출할 때는 images 라 부를거임
app.mount('/images',StaticFiles(directory=FILE_PATH),name='images')

@app.get('/download')
def download(filename:str):
    path = f'{FILE_PATH}/{filename}'
    if os.path.exists(path): # 만약에 이 경로가 존재 한다면
        return FileResponse(path, media_type='application/octet-stream',filename=filename)
    else:
        return {"msg":" 해당 파일을 다운로드 할 수 없습니다."}

@app.get('/files')
def get_files():
    # 특정 경로의 file 목록 확인
    file_list = os.listdir(FILE_PATH)
    logger.info(f'file list: {file_list}')
    return{'files':file_list}

@app.post('/upload')
def upload_file(files: List[UploadFile]):
    for file in files:
        logger.info(f'file name: {file.filename}')
        # 1. 저장경로 생성(폴더/파일)
        path = f'{FILE_PATH}/{file.filename}'
        # 2. file 로 부터 바이너리를 읽어서 저장
        # w 는 write, b 는 binary, + 는 읽기 쓰기 모두 가능
        with open(path, 'wb+') as file_obj:
            # file 에서 뽑아낸 file 객체, 경로에 있는 가상 파일 객체
            shutil.copyfileobj(file.file, file_obj)

    return {"msg": "upload가 완료되었습니다."}
'''
# 서버에서 하는 일
@app.post('/upload') # /upload 경로로 post 요청이 오면 실행된다.
def upload_file(files: List[UploadFile]): # files라는 이름으로 UploadFile의 List를 받음
    # 이때 files는 보내는 이름과 받는 이름이 동일해야함 (front에서 보내는 name="files"이기에 사용)
    for file in files: # 리스트로 부터 files를  file 이라는 변수에 하나씩 담아옴
        logger.info(f'file name: {file.filename}')
        # 1. 저장경로 생성(폴더/파일)
        path = f'{FILE_PATH}/{file.filename}' # path에 file 로 부터 filename을 얻어와서 저장할 경로를 생성
        # 2. file 로 부터 바이너리를 읽어서 저장
        # w 는 write, b 는 binary, + 는 읽기 쓰기 모두 가능
        with open(path, 'wb+') as file_obj: # open 을 이용해서 이 경로를 바이너리로 write 하는 옵션을 주어 이를 file_obj라는 변수에 담아준다. # with를 사용해서 open을 사용했을때 닫아주지 않아도 된다.
            # file 에서 뽑아낸 file 객체, 경로에 있는 가상 파일 객체
            shutil.copyfileobj(file.file, file_obj) # copyfileobj : 왼쪽에서 뽑아온 내용을 오른쪽에 있는 가상 파일 객체에다가 복사해주는 기능_실제롤 뽑아온 내용을 복사 -> 특정한 경로로 저장
            #copyfileobj를 사용해서 왼쪽의 file 에서 뽑아낸 file 객체를 오른쪽에 경로에 있는 file_obj라는 가상 파일 객체에 복사해주면 특정한 경로로 저장된다.
    return {"msg": "upload가 완료되었습니다."} # msg라는 이름으로 upload가 완료되었습니다. 라는 데이터를 front로 응답을 준다.
'''
@app.get('/')
def main():
    return {"msg": "This is main!!"}
