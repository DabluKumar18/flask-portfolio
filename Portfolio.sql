CREATE DATABASE portfolio_db;
USE portfolio_db;

CREATE TABLE contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    message TEXT
);

SELECT * FROM contact;

DESCRIBE contact;
