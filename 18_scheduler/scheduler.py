# 특정한 job을 어느시점에 수행할건지 지정
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from jobs import task1, task2, task3


def sch_start():
    # 1. 스케줄 객체 생성
    sch = AsyncIOScheduler()

    # 2. 스케줄러에 job 등록
    # 실행함수, 실행주기, 상세주기, 아이디, 매개변수(함수에서 사용할 경우)
    # 2-1. 단발성(1회성) 주기
    sch.add_job(task1,
        'date',
        run_date='2025-11-13 15:20:00',
        id='task1',
        args=['Fast API']
    )

    # 2-2. 주기적 실행(초,분,시)
    # seconds, minutes, hours
    sch.add_job(task2,'interval',seconds=10,id='task2',args=['News 사이트'])

    # 2-3. 주기적 실행(상세)
    # minute : 0~59, */5 (5분 간격)
    # hours : 0~23
    # day_of_week : 0~6(월-일), MON-SUN
    #day : 1~31
    #month : 1~12
    sch.add_job(task3,
        'cron',
        minute='*/1',
        day_of_week='MON-FRI',
        id='task3',
        args=['수집한 데이터']
    )



    return sch # 등록한 스케줄 객체를 반환