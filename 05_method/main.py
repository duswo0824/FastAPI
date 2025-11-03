from typing import Annotated, List

from fastapi import FastAPI, Body
from pydantic import BaseModel

from logger import Logger

app = FastAPI()
logger = Logger().get_logger(__name__)
logger.info('log 준비 완료')

# JSON 형태로 받을 예정인데, 아래 형태로는 JSON 인지 확신할 수 없음
# 그래서 전송되는 JSON 명시가 필요
class Item(BaseModel): # BaseModel을 상속 받는 class
    name: str
    price: float
    description: str | None = None
    tax: float | None = None
    color: List[str]
    spec: dict
    model_config = { # JSON 형태를 지정
        "json_schema_extra": { 
            "examples": [
                {
                    "name":"Notebook",
                    "price":35000,
                    "description":"very nice",
                    "tax":20,
                    "color":["red","white","blue","yellow"],
                    "spec":{"CPU":"octa core","RAM":"64GB","SSD":"1TB"}
                }
            ]
        }
    }

@app.get('/')
def main():
    return {'msg': 'main page'}

# post : 무언가를 입력 요청 할때 사용
# 일반적인 이름:값 은 문제없이 받을 수 있다.
# 하지만 이름:배열, 이름:오브젝트 와 같이 복잡한 형태는 JSON 형태로 받아야한다.
@app.post('/create/{item_id}')
# def create_item(item_id: int,item: Item): # 일반 형태
def create_item(item_id: int,item: Annotated[Item,Body(embed=True)]): # JSON 형태
    logger.info(f'받아온 item id: {item_id}')
    logger.info(f'item: {item}')
    # 입력 로직 수행(했다고 치자)
    return {'msg' : f'{item_id} 에 대한 입력이 성공 했습니다.',"item":item}

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

