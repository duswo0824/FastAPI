import time

from fastapi import FastAPI
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec #예상조건
from selenium.webdriver.support.wait import WebDriverWait
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from logger import Logger


app = FastAPI()
logger = Logger().get_logger(__name__)

app.mount("/view", StaticFiles(directory="view"), name="view")

# selenium driver 등록
driver_path = './drivers/chromedriver'

options = ChromiumOptions()
options.add_argument('--remote-allow-origin=*') # 이 옵션이 있어야 외부사이트 접속이 가능
options.add_argument('--start-maximized')       # 시작하자마자 브라우저 최대화(반응형 때문에)

@app.get("/search")
def search(keyword:str):
    job_list = []
    # 1. 드라이버 초기화
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    # 2. 페이지 열기
    url = 'https://www.saramin.co.kr/zf_user/search'
    url += f'?searchword={keyword}&recruitPage=1&recruitSort=closing_dt&recruitPageCount=20'
    driver.get(url)
    # 3. 가져오기
    elements = driver.find_elements(By.CSS_SELECTOR, '#recruit_info_list div.content div.item_recruit')
    logger.info(len(elements))

    for elem in elements:
        # elem 을 통해 find_element() 나 find_elements() 을 이용해 새로운 elem 을 추출할 수 있다.
        a_tag = elem.find_element(By.CSS_SELECTOR, 'div.area_job h2.job_tit a')
        title = a_tag.text
        link = a_tag.get_attribute('href')
        date = elem.find_element(By.CSS_SELECTOR, 'div.area_job div.job_date span.date')
        job_list.append({'title': title, 'date': date.text, 'link': link})

    # 자원 반납
    driver.quit()

    return {'list': job_list}

@app.post('/saramin_login') # /docs로 test 가능
def saramin_login(id:str, pw:str):
# 1. 드라이버 초기화
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    # 2. 페이지 열기
    url = 'https://www.saramin.co.kr/zf_user/auth'
    driver.get(url) # get방식으로 url을 열어줌
    # 3. 원하는 요소 가져와서 특정 기능 수행(클릭,스크롤,입력)
    driver.find_element(By.ID,'id').send_keys(id)
    driver.find_element(By.ID,'password').send_keys(pw)
    time.sleep(1) # 1초 대기
    driver.find_element(By.CSS_SELECTOR, 'button.btn_login.BtnType.SizeML[type="submit"]').click()

    # 로그인 페이지로 이동했을 때 페이지가 다 읽혀지지 않았을 경우가 있다.
    # 그래서 여유있게 sleep을 주면 된다.
    # time.sleep(3)
    #특정 요소가 읽혀질때 까지 기다리게 하는 방법도 있다.
    # WebDriverWait(driver,최대 대기시간).until(기다리는 요소)
    gnb = (WebDriverWait(driver, 3)
           .until(ec.presence_of_element_located((By.CSS_SELECTOR, '#sri_gnb_wrap ul.gnb'))))
    logger.info(f'gnb:{gnb}')
    # javascript 강제 실행
    driver.execute_script(f'alert("안녕하세요 {id}님! 사람인 입니다.")')

    time.sleep(3)
    driver.switch_to.alert.accept() # alert을 자동으로 닫아주는 기능

    list = gnb.find_elements(By.CSS_SELECTOR, 'li.only a')
    for item in list:
        logger.info(f'item:{item.text}')
        if item.text == '스크랩/관심기업':
            item.click()


@app.get("/")
def root():
    return RedirectResponse("/view/index.html")