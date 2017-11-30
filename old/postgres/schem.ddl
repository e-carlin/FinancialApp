psql postgres
CREATE ROLE banterapiuser WITH LOGIN PASSWORD 'db_user_22';
CREATE DATABASE banter;
GRANT ALL PRIVILEGES ON DATABASE banter TO banterapiuser;
\connect banter

CREATE TABLE users (
	id 			BIGSERIAL PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    email       TEXT NOT NULL, # ADD UNIQUE CONSTRAINT
    password    TEXT NOT NULL
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO banterapiuser;

INSERT INTO users (first_name, last_name, email, password) VALUES('evan','carlin','evan@carlin.com','123');
