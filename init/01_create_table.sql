-- クラステーブル
CREATE TABLE classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL
);

-- 教科テーブル
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL
);

-- 教師テーブル
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    teacher_name VARCHAR(100) NOT NULL
);

-- 教室テーブル
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(50) NOT NULL
);

-- クラス別教科情報テーブル
CREATE TABLE class_subject_info (
    class_subject_info_id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(class_id),
    subject_id INTEGER REFERENCES subjects(subject_id),
    teacher_id INTEGER REFERENCES teachers(teacher_id),
    room_id INTEGER REFERENCES rooms(room_id),
    UNIQUE(class_id, subject_id)
);

-- 週タイプテーブル
CREATE TABLE week_types (
    week_type_id SERIAL PRIMARY KEY,
    week_type CHAR(1) NOT NULL CHECK (week_type IN ('A', 'B', 'C', 'D')),
    UNIQUE(week_type)
);

-- 時間割テーブル
CREATE TABLE schedules (
    schedule_id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(class_id),
    week_type_id INTEGER REFERENCES week_types(week_type_id),
    day_of_week INTEGER CHECK (day_of_week BETWEEN 1 AND 7),
    period INTEGER,
    class_subject_info_id INTEGER REFERENCES class_subject_info(class_subject_info_id),
    UNIQUE(class_id, week_type_id, day_of_week, period)
);

-- 年間スケジュールテーブル
CREATE TABLE yearly_schedule (
    yearly_schedule_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    week_number INTEGER CHECK (week_number BETWEEN 1 AND 53),
    week_type_id INTEGER REFERENCES week_types(week_type_id),
    UNIQUE(year, week_number)
);

-- 週タイプの初期データを挿入
INSERT INTO week_types (week_type) VALUES ('A'), ('B'), ('C'), ('D');