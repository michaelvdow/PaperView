#CREATE DATABASE IF NOT EXISTS TempDB;
#USE TempDB;

CREATE DATABASE IF NOT EXISTS googleScholar;
USE googleScholar;

CREATE TABLE IF NOT EXISTS test(
id INTEGER PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS Author(
    AuthorId INTEGER PRIMARY KEY AUTO_INCREMENT,
    Name TEXT NOT NULL,
    Affiliation TEXT,
    CitedBy INTEGER,
    #Email TEXT,  # right?
    HIndex INTEGER,
    I10Index INTEGER
);

CREATE TABLE IF NOT EXISTS Article(
    ArticleId INTEGER PRIMARY KEY AUTO_INCREMENT,
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

DELIMITER //
CREATE TRIGGER CitationUpdate
AFTER INSERT ON Citation FOR EACH ROW
BEGIN
    DECLARE citedAuthorId INTEGER;
    
	SET @citedAuthorId = (SELECT PrimaryAuthorId FROM Article WHERE ArticleId = NEW.Cites);
	
    UPDATE Article SET Citations = Citations + 1 WHERE ArticleId = NEW.Article;
    UPDATE Article SET CitedBy = CitedBy + 1 WHERE ArticleId = NEW.Cites;

    UPDATE Author SET CitedBy = CitedBy + 1 WHERE AuthorId = citedAuthorId;

END//
DELIMITER ;