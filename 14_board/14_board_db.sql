create table bbs(
	idx int(8) primary key auto_increment
	,subject varchar(50)
	,content longtext
	,user_name varchar(50)
	,b_hit int(8) default 0 -- 조회수
	,reg_date date default current_date()
);

show databases;

-- DROP TABLE bbs;

select*from bbs;
select idx,subject,user_name,reg_date,b_hit from bbs order by idx desc;

insert into bbs(subject,user_name,content)
values('테스트 제목','admin','abcde');

-- delete from bbs;

-- SELECT COUNT(id) FROM member WHERE id = :id AND pw = :pw; 
-- 대문자가 여기 사이트에 기본 값 소문자가 내가 만든것