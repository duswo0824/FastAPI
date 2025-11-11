select*from bbs;

insert into bbs(subject,user_name,content)values(:subject,:user_name,:content);
insert into photo(ori_filename,new_filename,idx)values(:ori_filename,:new_filename,:idx);

create table photo (
    file_idx int(8) primary key auto_increment,
    ori_filename varchar(100),
    new_filename varchar(100),
    idx int(8),
    foreign key(idx) references bbs(idx)
);

desc photo;

-- bbs 에 다음과 같은 내용을 넣으려고 한다.
-- subject : 파일올리기
-- user_name : 테스터
-- content : 글도 올리고 파일도 올리고
insert into bbs(subject,user_name,content)values('파일올리기','테스터','글도 올리고 파일도 올리고');
select*from bbs;

-- 그리고 photo에 사진을 한장 올리려고 한다.
-- ori_filename : test.png
-- new_filename : 123456789.png
insert into photo(ori_filename,new_filename,idx)values('test.png','123456789.png',3);
select*from photo;

select * from bbs where idx = 7;
select * from photo where idx = 7;

update bbs set b_hit = b_hit+1 where idx = 7;

ALTER TABLE bbs AUTO_INCREMENT = 7; -- 다음 번호를 7로 시작
ALTER TABLE photo AUTO_INCREMENT = 7;
-- 삭제하기 순서
-- 삭제할 파일 이름
select new_filename from photo where idx = 7;

-- delete photo; -- photo 가 자식이기 때문에 먼저 지워져야함
delete from photo where idx = 7;

-- delete bbs; -- 부모 마지막에
delete from bbs where idx = 7;
