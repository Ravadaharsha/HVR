CREATE TABLE jee_cutoff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_name VARCHAR(255),
    academic_program_name VARCHAR(255),
    seat_type VARCHAR(50),
    quota VARCHAR(50),
    gender VARCHAR(50),
    closing_rank INT
);
CREATE TABLE jee_cutoff_predicted (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_name VARCHAR(255),
    academic_program_name VARCHAR(255),
    seat_type VARCHAR(50),
    quota VARCHAR(50),
    gender VARCHAR(50),
    closing_rank INT
);
