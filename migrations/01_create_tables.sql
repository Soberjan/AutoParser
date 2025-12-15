CREATE TABLE IF NOT EXISTS applicant (
	id SERIAL PRIMARY KEY,
	"name" varchar,
	phone varchar,
    CONSTRAINT unique_name_phone UNIQUE ("name", phone),
	email varchar,
	city varchar,
	birth_date varchar
);
CREATE TABLE IF NOT EXISTS vacancy (
	id SERIAL PRIMARY KEY,
	vacancy varchar,
    "category" varchar,
    salary float,
    "status" varchar,
    region varchar,
    opened_at date,
    closed_at date,
    CONSTRAINT chk_vacancy_dates CHECK (
        closed_at IS NULL OR opened_at IS NULL OR closed_at >= opened_at
    ),
    deadline_date date,
    CONSTRAINT unique_id UNIQUE (vacancy)
);
CREATE TABLE IF NOT EXISTS cv_binary (
	id SERIAL PRIMARY KEY,
    binary_file varchar
);
CREATE TABLE IF NOT EXISTS cv (
	id SERIAL PRIMARY KEY,
    applicant_id int REFERENCES applicant(id) ON DELETE CASCADE,
	vacancy_id int REFERENCES vacancy (id) ON DELETE CASCADE,
    CONSTRAINT unique_applicant_vacancy UNIQUE (applicant_id, vacancy_id),
    salary float,
    other varchar,
    cv_binary_id int REFERENCES cv_binary (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS skill (
	id SERIAL PRIMARY KEY,
	"name" varchar,
    CONSTRAINT unique_skill UNIQUE ("name")
);
CREATE TABLE IF NOT EXISTS cv_skill (
    id SERIAL PRIMARY KEY,
    cv_id int REFERENCES cv (id) ON DELETE CASCADE,
	skill_id int REFERENCES skill (id) ON DELETE CASCADE,
    CONSTRAINT unique_cv_skill UNIQUE (cv_id, skill_id)
);
CREATE TABLE IF NOT EXISTS vacancy_skill (
    id SERIAL PRIMARY KEY,
    vacancy_id int REFERENCES vacancy (id) ON DELETE CASCADE,
	skill_id int REFERENCES skill (id) ON DELETE CASCADE,
    CONSTRAINT unique_vacancy_skill UNIQUE (vacancy_id, skill_id)
);

CREATE TABLE IF NOT EXISTS education (
	id SERIAL PRIMARY KEY,
    cv_id int NOT NULL REFERENCES cv (id) ON DELETE CASCADE,
    institute VARCHAR,
    major VARCHAR,
    degree VARCHAR,
    "start_date" DATE,
    "end_date" DATE,
    CONSTRAINT chk_education_dates CHECK (
        "end_date" IS NULL OR "start_date" IS NULL OR "end_date" >= "start_date"
    ),
    CONSTRAINT unique_education UNIQUE (institute, major, degree, "start_date", "end_date", cv_id)
    
);

CREATE TABLE IF NOT EXISTS experience (
	id SERIAL PRIMARY KEY,
    cv_id int REFERENCES cv (id) ON DELETE CASCADE,
    company VARCHAR,
    position VARCHAR,
    "start_date" DATE,
    "end_date" DATE,
    CONSTRAINT chk_experience_dates CHECK (
        "end_date" IS NULL OR "start_date" IS NULL OR "end_date" >= "start_date"
    ),
    "category" VARCHAR,
    CONSTRAINT unique_experience UNIQUE (company, position, "start_date", "end_date", cv_id)
);

CREATE TABLE IF NOT EXISTS progress (
	id SERIAL PRIMARY KEY,
    cv_id int REFERENCES cv (id) ON DELETE CASCADE,
    "status" text NOT NULL CHECK (status IN ('подал заявку', 'проходит собеседование', 'принят', 'отклонен', 'архивирован')),
    "start_date" DATE,
    "end_date" DATE,
    CONSTRAINT chk_progress_dates CHECK (
        "end_date" IS NULL OR "start_date" IS NULL OR "end_date" >= "start_date"
    ),
    CONSTRAINT unique_progress UNIQUE (id)
);
