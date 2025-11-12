import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from logger import Logger

app = FastAPI()

logger = Logger().get_logger(__name__)

app.mount('/view', StaticFiles(directory='view'), name='view')

@app.get("/")
def root():
    return RedirectResponse(url='/view/index.html')

@app.get("/search")
async def search(keyword: str):
    logger.info(f"keyword: {keyword}")
    url = 'https://www.saramin.co.kr/zf_user/search'
    params = {
        'searchword': keyword,
        'recruitPage':1,
        'recruitSort':'closing_dt',
        'recruitPageCount':20
    }

    # await 은 실제적인 비동기 처리를 하는 함수에 붙인다.
    # await 을 실행하는 상위 함수는 async가 있어야 한다.
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params) # 해당 주소의 전체 페이지
        # logger.info(f'resp: {resp.text}')
        # html.parser - 가장 일반적인 파서
        # lxml - C 로 만들어진 속도가 빠른 파서(pip install lxml)
        # html5lib - 웹표준 기반 파서(pip install html5lib), 정확도가 높지만 속도가 느리다.
        soup = BeautifulSoup(resp.content, 'html.parser')
        elements = soup.select('#recruit_info_list div.content div.item_recruit')
        logger.info(f'elements: {len(elements)}') # len의 수가 20이면 정상

        info_list = []

        for elem in elements:
            # logger.info(f'element: {elem}')
            a_tag = elem.select_one('div.area_job h2.job_tit a')
            # elem 을 통해 select() 나 select_one()을 이용해 새로운 elem을 추출할 수 있다.
            # logger.info(f'a_tag: {a_tag}')
            title = a_tag.text # text : 태그와 태그사이
            link = a_tag['href']
            date = elem.select_one('div.area_job div.job_date span.date')
            # logger.info(f'title:{title},date: {date.text}, link: {link}')
            info_list.append({'title': title, 'date': date.text, 'link': link})

    return {'list': info_list}
