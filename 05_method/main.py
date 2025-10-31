from fastapi import FastAPI

from logger import Logger

app = FastAPI()
logger = Logger().get_logger(__name__)
logger.info('log 준비 완료')

@app.get('/')
def main():
    return {'msg': 'main page'}

# post : 무언가를 입력 요청 할때 사용
@app.post('/create/{item_id}')
def create_item(item_id: int):
    logger.info(f'받아온 item id: {item_id}')
    # 입력 로직 수행(했다고 치자)
    return {'msg' : f'{item_id} 에 대한 입력이 성공 했습니다.'}

# put : 데이터를 수정 요청 할때 주로 사용
@app.put('/update/{item_id}')
def update_item(item_id: int):
    logger.info(f'받아온 item id: {item_id}')
    # 수정 로직 수행(했다고 치자)
    return {'msg' : f'{item_id} 에 대한 수정에 성공 했습니다.'}

# delete : 데이터 삭제 요청 할때 주로 사용
@app.delete('/delete/{item_id}')
def delete_item(item_id: int):
    logger.info(f'받아온 item id: {item_id}')
    # 삭제 로직 수행(했다고 치자)
    return {'msg': f'{item_id} 에 대한 삭제에 성공 했습니다.'}