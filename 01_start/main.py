from fastapi import FastAPI

# FastAPI를 사용하겠다는 선언
app = FastAPI()

# 요청이 get 방식으로 http://domain:port/ 로 오면...
@app.get("/")
def main(): # 이 함수가 실행된다.
    # 아래 내용을 클라이언트로 전송
    # JSON 형태에 가까운 dictionary를 사용
    return {"message": "Hello, FastAPI! MY name is Lee,yeon-jae"}