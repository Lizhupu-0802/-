DELETE FROM plant_grade;
DELETE FROM course;
DELETE FROM student;
DELETE FROM plant;

INSERT INTO student (sn, no, name)  VALUES
    (101, 'S001',  '张三'),
    (102, 'S002',  '李四'),
    (103, 'S003',  '王五'),
    (104, 'S004',  '马六');

INSERT INTO course (sn, no, name, score, attr)  VALUES
    (101, 'C01',  '高数', 5, '必修'),
    (102, 'C02',  '外语', 5, '必修'),
    (103, 'C03',  '线代', 3, '选修');


INSERT INTO plant (sn, cou_sn, semester, week, class_time, class_position)  VALUES
    (10000, 101, '2020-2021学年秋',  '1-18周', '周一1-2节', '一公教D103'),
    (10001, 102, '2020-2021学年秋',  '3-18周', '周三5-6节', '一公教A111'),
    (10002, 103, '2020-2021学年秋',  '3-18周', '周四5-6节', '一公教B305'),
    (10003, 101, '2020-2021学年秋',  '3-18周', '周五1-2节', '一公教B209'),
    (10004, 102, '2020-2021学年秋',  '4-18周双周', '周二7-8节', '一公教D103'),
    (10005, 103, '2020-2021学年秋',  '4-18周', '周二1-2节', '一公教A219');

INSERT INTO plant_grade (pla_sn, stu_sn, grade)  VALUES
(10000, 101,  91),
(10002, 101,  89),
(10005, 102,  89);