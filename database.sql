DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS books;

CREATE TABLE students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fullname TEXT NOT NULL,
  student_id TEXT UNIQUE NOT NULL
);

CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
)