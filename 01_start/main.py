from fastapi import FastAPI

# FastAPI를 사용하겠다는 선언
app = FastAPI()

# 요청이 get 방식으로 http://domain:port/ 로 오면...
@app.get("/")
def main(): # 이 함수가 실행된다.
    # 아래 내용을 클라이언트로 전송
    # JSON 형태에 가까운 dictionary를 사용
    return {"message": "Hello, FastAPI! MY name is Lee,yeon-jae"}
# uvicorn : 서버 프로그램 이름
# main:app - main.py에 있는 app 사용
# --host = 0.0.0.0 - 모든 IP 허용(이게 없으면 localhost, 127.0.0.1 만 허용)
# --port = 3000 - 이 서버의 포트를 3000번으로 지정하겠다.
# --reload - 소스 변경시 자동으로 서버를 재시작하겠다.
# uvicorn main:app --host=0.0.0.0 --port=3000 --reload
