DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student  (
    sn       INTEGER,     --序号
    no       VARCHAR(10), --学号
    name     TEXT,        --姓名
    gender   CHAR(1),     --性别(F/M/O)
    enrolled DATE,        --入学时间
    PRIMARY KEY(sn)
);

-- 给sn创建一个自增序号
CREATE SEQUENCE seq_student_sn 
    START 10000 INCREMENT 1 OWNED BY student.sn;
ALTER TABLE student ALTER sn 
    SET DEFAULT nextval('seq_student_sn');
-- 学号唯一
CREATE UNIQUE INDEX idx_student_no ON student(no);

-- === 课程表
DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course  (
    sn       INTEGER,     --序号
    no       VARCHAR(10), --课程号
    name     TEXT,        --课程名称
    score    INTEGER,     --课程学分
    attr     TEXT,        --课程属性
    PRIMARY KEY(sn)
);
CREATE SEQUENCE seq_course_sn 
    START 10000 INCREMENT 1 OWNED BY course.sn;
ALTER TABLE course ALTER sn 
    SET DEFAULT nextval('seq_course_sn');
CREATE UNIQUE INDEX idx_course_no ON course(no);


DROP TABLE IF EXISTS plant;
CREATE TABLE  IF NOT EXISTS plant (
    sn INTEGER,         -- 计划编号
    cou_sn INTEGER,     -- 课程序号
    semester TEXT,      -- 学期
    week TEXT,          -- 周次
    class_time TEXT,          -- 时间
    class_position TEXT,       -- 地点
    PRIMARY KEY(sn)
);
CREATE SEQUENCE seq_plant_sn
    START 10000 INCREMENT 1 OWNED BY plant.sn;
ALTER TABLE plant ALTER sn
    SET DEFAULT nextval('seq_plant_sn');

ALTER TABLE plant
    ADD CONSTRAINT  cou_sn_fk FOREIGN KEY (cou_sn) REFERENCES course(sn);




DROP TABLE IF EXISTS plant_grade;
CREATE TABLE IF NOT EXISTS plant_grade  (
    stu_sn INTEGER,     -- 学生序号
    pla_sn INTEGER,     -- 课程序号
    grade  NUMERIC(5,2), -- 最终成绩
    PRIMARY KEY(stu_sn, pla_sn)
);

ALTER TABLE plant_grade
    ADD CONSTRAINT stu_sn_fk FOREIGN KEY (stu_sn) REFERENCES student(sn);
ALTER TABLE plant_grade
    ADD CONSTRAINT pla_sn_fk FOREIGN KEY (pla_sn) REFERENCES plant(sn);
