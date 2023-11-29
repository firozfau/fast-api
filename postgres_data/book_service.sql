-- Drop the database if it exists
DROP DATABASE IF EXISTS book_service;

-- Create the database
CREATE DATABASE book_service;

DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
  id SERIAL PRIMARY KEY,
  full_name varchar(150) NOT NULL,
  gender int DEFAULT 1,
  status int NOT NULL DEFAULT 1
);

DROP TABLE IF EXISTS book_information;
CREATE TABLE book_information (
  id SERIAL PRIMARY KEY,
  title varchar(250) NOT NULL,
  author_id int NOT NULL,
  status int DEFAULT 1,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES authors (id)
);

DROP TABLE IF EXISTS client_information;
CREATE TABLE client_information (
  id SERIAL PRIMARY KEY,
  full_name varchar(150) NOT NULL,
  gender int DEFAULT 1,
  status int DEFAULT 1,
  dob date
);

DROP TABLE IF EXISTS borrowed_information;
CREATE TABLE borrowed_information (
  id SERIAL PRIMARY KEY,
  book_id int NOT NULL,
  client_id int NOT NULL,
  borrowed_date date NOT NULL,
  return_date date,
  comments varchar(250),
  status int DEFAULT 1,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  created_id int,
  updated_date timestamp DEFAULT CURRENT_TIMESTAMP,
  expected_return_date date NOT NULL,
  FOREIGN KEY (book_id) REFERENCES book_information (id),
  FOREIGN KEY (client_id) REFERENCES client_information (id)
);