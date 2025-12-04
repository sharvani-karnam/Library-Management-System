CREATE DATABASE IF NOT EXISTS library_management;
USE library_management;

-- Table for storing book details
CREATE TABLE IF NOT EXISTS book_details (
    Book_id INT PRIMARY KEY,
    Title VARCHAR(255),
    Authors_Name VARCHAR(255),
    Genre VARCHAR(100),
    Copies INT
);

-- Table for library card holders
CREATE TABLE IF NOT EXISTS library_card (
    Card_No INT PRIMARY KEY,
    Readers_Name VARCHAR(255),
    BranchAddress VARCHAR(255),
    Subscription INT
);

-- Table for tracking borrowed books
CREATE TABLE IF NOT EXISTS borrower (
    Borrower_id INT AUTO_INCREMENT PRIMARY KEY,
    Card_No INT,
    Name VARCHAR(255),
    Address VARCHAR(255),
    Phone VARCHAR(20),
    Book_ID INT,
    Issued_Date DATE,
    Return_Date DATE,
    FOREIGN KEY (Book_ID) REFERENCES book_details(Book_id)
);