import os
import shutil
import uuid

from fastapi import params

from util.database import get_db
from util.logger import Logger
from sqlalchemy import text

logger = Logger().get_logger(__name__)

# 게시판에 관련된 기능
def list(session):
    login_id = session.get('loginId','')
    logger.info(f'login id:{login_id}')
    db = None
    list = []

    if login_id == '':
        return {'list':list,'login':login_id}

    sql = text('''SELECT idx,subject,user_name,reg_date,b_hit 
                    FROM bbs ORDER BY idx DESC;''')

    try :
        db = get_db()
        list = db.execute(sql).mappings().fetchall()
        logger.info(f'list = {list}')
    except Exception as e :
        logger.error(e)
    finally:
        db.close()
        return {'list':list,'login':login_id}


def file_save(files):
    file_list = []
    for file in files:
        ori_filename = file.filename
        # img01.png -> 12345678.png (확장자는 유지)
        ext = os.path.splitext(ori_filename)[1] # img01.png -> [img01,.png] 1번인덱스에 확장자
        new_filename = f'{uuid.uuid4()}{ext}'

        with open('upload/'+new_filename,'wb') as tmp:
            shutil.copyfileobj(file.file,tmp)

        file_list.append({'ori_filename':ori_filename,'new_filename':new_filename})
        logger.info(f'file_list = {file_list}')
    return file_list

def write(subject, user_name, content, files):
    result = {'success':'false'}
    # bbs 에 subject, user_name, content 저장
    sql = text('insert into bbs (subject,user_name,content)values(:subject,:user_name,:content)')
    params = {'subject':subject, 'user_name':user_name, 'content':content}
    conn = get_db()
    try:
         exec_result = conn.execute(sql, params)
         # exec_result.rowcount = 영향받은 데이터 수
         # logger.info(f'exec_result = {exec_result.rowcount}')
         # exec_result.lastrowid = 가장 마지막 row rkqt
         logger.info(f'exec_result:{exec_result.lastrowid}')
         if exec_result.rowcount > 0:
             result['success'] = 'true'
             # 파일들을 전달하면 저장하고 생성된 새로운 이름을 받는다.
             file_list = file_save(files)
             # 파일의 이름, 새로 생성된 이름, idx를  photo 에 저장
             sql = text('insert into photo(ori_filename,new_filename,idx)values(:ori_filename,:new_filename,:idx)')
             for file in file_list:
                 file['idx'] = exec_result.lastrowid
                 conn.execute(sql, file)
             conn.commit()
    except Exception as e:
        logger.error(e)
        conn.rollback()
    finally:
        conn.close()
        return result
