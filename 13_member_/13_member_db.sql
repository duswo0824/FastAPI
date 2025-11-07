-- member 라는 이름의 테이블을 생성
create table member(
	id varchar(50) primary key -- 회원 아이디: 최대 50자 문자열, 기본키(중복 불가, NULL 불가)
	,pw varchar(100) -- 비밀번호: 최대 100자 문자열 (암호화 저장을 고려한 여유 길이)
	,name varchar(50) -- 이름: 최대 50자 문자열
	,age int(3) -- 나이: 정수형 (3)
	,gender varchar(4) -- 성별: 문자열
	,email varchar(100) -- 이메일: 최대 100자 문자열
);

-- 테이블의 구조를 확인하는 명령 (컬럼명, 타입, 키 정보 등을 보여줌)
desc member;

-- member 테이블의 모든 행을 조회하는 SQL
select*from member;

-- id가 '' 인 데이터 삭제
delete from member where id = 'duswo';

select count(id) as cnt from  member where id = 'admin'; -- 0이면 없는것 1이면 있는것

select count(id) as cnt from member where id = 'admin' and pw = 'pass';

select id,name,gender from member;