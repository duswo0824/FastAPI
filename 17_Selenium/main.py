from fastapi import FastAPI
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from logger import Logger

app = FastAPI()
logger = Logger().get_logger(__name__)

app.mount("/view", StaticFiles(directory="view"), name="view")

# selenium driver 등록
driver_path = './driver/chromedriver.exe'

options = ChromiumOptions()
options.add_argument('--remote-allow-origins=*') # 이 옵션이 있어야 외부사이트 접속이 가능
options.add_argument('--start-maximized') # 시작하자마자 브라우저 최대화(반응형 때문에)

@app.get("/search")
def search(keyword: str):
    job_list = []
    # 1. 드라이버 초기화
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    # 2. 페이지 열기
    url = 'https://www.saramin.co.kr/zf_user/search'
    url += f'?searchword={keyword}&recruitPage=1&recruitSort=closing_dt&recruitPageCount=20'
    driver.get(url)
    # 3. 가져오기
    elements = driver.find_elements(By.CSS_SELECTOR,'#recruit_info_list div.content div.item_recruit')
    logger.info(len(elements))

    for elem in elements:
        #  elem 을 통해 find_element() 나 find_elements()을 이용해 새로운 elem을 추출할 수 있다.
        a_tag = elem.find_element(By.CSS_SELECTOR,'div.area_job h2.job_tit a')
        title = a_tag.text
        link = a_tag.get_attribute('href')
        date = elem.find_element(By.CSS_SELECTOR,'div.area_job div.job_date span.date')
        job_list.append({'title': title, 'date': date.text, 'link': link})

    # 자원 반납
    driver.quit()

    return {'list': job_list}

@app.get("/")
def root():
    return RedirectResponse(url='/view/index.html')
