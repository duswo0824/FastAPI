from fastapi import FastAPI

from scheduler import sch_start

sch = sch_start() # 스케줄 객체 불러오기
app = FastAPI() # 앱 실행

@app.get("/")
@app.get("/start")
async def start():
    sch.start()
    return {'msg':'scheduler 실행!'}

@app.get("/stop")
async def stop():
    sch.shutdown()
    return {'msg':'scheduler 정지'}

@app.get("/job/pause/{id}")
def pause_job(id:str):
    sch.pause_job(id)
    return {'msg':f'{id} Job 일시정지'}

@app.get("/job/resume/{id}")
def resume_job(id:str):
    sch.resume_job(id)
    return {'msg':f'{id} Job 다시실행'}