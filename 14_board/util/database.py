from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 접속 정보
id = 'web_user'
pw = 'pass'
host = 'localhost'
port = 3306
db = 'mydb'
url = f'mysql+pymysql://{id}:{pw}@{host}:{port}/{db}'

# 엔진 생성 _ autocommit=False 기본값
engine = create_engine(url, echo=True, pool_size=1)

# 세션 생성
session = sessionmaker(bind=engine)

def get_db(): # 함수 실행
    return session()
