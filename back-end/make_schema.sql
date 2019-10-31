CREATE DATABASE IF NOT EXISTS TempDB;
USE TempDB;
CREATE TABLE IF NOT EXISTS test(
       id INTEGER PRIMARY KEY AUTO_INCREMENT,
       name VARCHAR(32)
);

CREATE DATABASE IF NOT EXISTS googleScholar;
USE googleScholar;
CREATE TABLE IF NOT EXISTS InterestedIn(
    AuthorId INTEGER, 
    Interest VARCHAR(255), 
    PRIMARY KEY (AuthorId, Interest), 
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorId)
);

CREATE TABLE IF NOT EXISTS YearlyCitations(
    AuthorId INTEGER, 
    Year INTEGER, 
    Citations INTEGER NOT NULL, 
    PRIMARY KEY (AuthorId, Year),
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorId)
);

CREATE TABLE IF NOT EXISTS Article(
    ArticleId INTEGER PRIMARY KEY,
    PrimaryAuthorId INTEGER, 
    CitedBy INTEGER, 
    Citations INTEGER, 
    Title TEXT NOT NULL, 
    Year INTEGER, 
    Url TEXT, 
    Publisher TEXT, 
    Journal TEXT, 
    FOREIGN KEY (PrimaryAuthorId) REFERENCES Author(AuthorId)
);

CREATE TABLE IF NOT EXISTS Author(
    AuthorId INTEGER PRIMARY KEY, 
    Name TEXT NOT NULL, 
    Affiliation TEXT, 
    CitedBy INTEGER, 
    HIndex INTEGER, 
    I10Index INTEGER
);