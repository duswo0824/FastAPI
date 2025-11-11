import os.path
import shutil
import uuid

from util.database import get_db
from util.logger import Logger
from sqlalchemy import text

logger = Logger().get_logger(__name__)

# 게시판에 관련된 기능
def list(session):
    login_id = session.get('loginId','')
    logger.info(f'loginId = {login_id}')
    db = None
    list = []
    if login_id == '':
        return {'list':list, 'login':''}

    sql = text("""SELECT 
            idx,subject,user_name,reg_date,b_hit 
        FROM bbs ORDER BY idx DESC""")
    try:
        db = get_db()
        list = db.execute(sql).mappings().fetchall()
        logger.info(f'list = {list}')
    except Exception as e:
        logger.error(e)
    finally:
        db.close()
        return {'list':list, 'login':login_id}


def file_save(files):
    file_list = []
    for file in files:
        ori_filename = file.filename
        # img01.png -> 123456798.png
        ext = os.path.splitext(ori_filename)[1] # img01.png -> [img01, .png]
        new_filename = f'{uuid.uuid4()}{ext}'
        with open('upload/'+new_filename, 'wb') as tmp:
            shutil.copyfileobj(file.file, tmp)

        file_list.append({'ori_filename':ori_filename, 'new_filename':new_filename})
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
         # exec_result.lastrowid = 가장 마지막 row 값 == 방금넣은 idx 값
         logger.info(f'exec_result = {exec_result.lastrowid}')
         if exec_result.lastrowid > 0:
             result['success'] = 'true'
             # 파일들을 전달하면 저장하고 생성된 새로운 이름을 받는다.
             file_list = file_save(files)
             # 파일의 이름, 새로생성된이름, idx 를 photo 에 저장
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

def detail(login_id, idx):
    post = {}
    photos = []
    # login 체크
    if login_id == '':
        return{'login':login_id, 'post':post,'photos':photos}

    conn = get_db()
    try:
        # 게시글 가져오기
        sql = text('SELECT * FROM bbs WHERE idx=:idx')
        post = conn.execute(sql, {'idx':idx}).mappings().fetchone()
        # 사진 리스트 가져오기
        sql = text('SELECT * FROM photo WHERE idx=:idx')
        photos = conn.execute(sql, {'idx':idx}).mappings().fetchall()
        # 조회수 올리기
        sql = text('UPDATE bbs SET b_hit = b_hit+1 WHERE idx =:idx')
        exec_result = conn.execute(sql, {'idx':idx})
        logger.info(f'updated row = {exec_result.rowcount}')
        # 결과값 반환
        conn.commit()
        pass
    except Exception as e:
        logger.error(e)
        conn.rollback()
    finally:
        return{'login':login_id, 'post':post,'photos':photos}

def delete(idx):
    conn = get_db()

    try:
        # idx 에 해당하는 파일명
        sql = text('SELECT new_filename FROM photo WHERE idx=:idx')
        photos = conn.execute(sql, {'idx':idx}).mappings().fetchall()

        # photo 에서 해당 idx 를 가지고 있는 데이터 삭제(자식)
        sql = text('DELETE FROM photo WHERE idx=:idx')
        exec_result = conn.execute(sql, {'idx':idx})
        logger.info(f'deleted row : {exec_result.rowcount}')

        # bbs 에서 해당 idx 를 가지고 있는 데이터 삭제(부모)
        sql = text('DELETE FROM bbs WHERE idx=:idx')
        conn.execute(sql, {'idx':idx})

        # 진짜 파일 삭제
        for name in photos:
            path = f'upload/{name.new_filename}'
            logger.info(f'path = {path}')
            if os.path.exists(path): # os : 기본 경로
                logger.info('exists!!')
                os.remove(path)
        conn.commit()
    except Exception as e:
        logger.error(e)
        conn.rollback()
    finally:
        conn.close()

def update(login_id, subject, idx, content, files):
    success = False

    if login_id == '':
        return {'login': login_id, 'success': success}

    conn = get_db()

    try:
        # update 구문 실행
        sql = text('UPDATE bbs SET subject=:subject, content=:content WHERE idx=:idx')
        conn.execute(sql, {'subject': subject, 'content': content, 'idx': idx})

        # upload 파일이 있는지 확인
        if len(files) > 0:
            file_list = file_save(files)  # files 를 주면 저장 후 원래파일명, 변경된 파일명 리스트를 반환한다.
            # 있으면 photo 에 저장 -> DB 에 저장
            sql = text('INSERT INTO photo(ori_filename,new_filename,idx)VALUES(:ori_filename,:new_filename,:idx)')
            for file in file_list:
                file['idx'] = idx
                conn.execute(sql, file)

        conn.commit()
        success = True
    except Exception as e:
        logger.error(e)
        conn.rollback()
    finally:
        conn.close()
        return {'login': login_id, 'success': success}