from server.paperview import graph_driver
import sqlite3
import time
import ast
import pymysql.cursors

def insertAuthors(mysqlConn, graphConn):
    seconds = time.time()
    cursor = mysqlConn.cursor()
    cursor.execute('SELECT * FROM Author')
    i = 0
    for row in cursor:
        # Progress
        if i % 1000 == 0:
            print(i/5530376*100)
        i += 1
        authorId = row[0]
        name = row[1]
        try:
            graphConn.insert_new_author(authorId, name)
        except:
            pass 
    print("FINISHED!")
    finalSeconds = time.time()
    print("Seconds to run: " + str(finalSeconds - seconds))

def insertWroteRelations(liteConn, mysqlConn, graphConn):
    seconds = time.time()
    liteCur = liteConn.cursor()
    liteCur.execute('SELECT * FROM googlescholararticles')
    mysqlCur = mysqlConn.cursor()
    i = 0
    for row in liteCur:
        # Progress, last stopped at 16.3
        if i % 1000 == 0:
            print(i/2000000*100)
        i += 1

        articleId = row[0]
        title = row[4]
        writers = []

        # Find primary author id
        primaryAuthorName = row[1]
        if primaryAuthorName != None:
            mysqlCur.execute("SELECT AuthorId FROM Author WHERE Name = %s", [primaryAuthorName])
            primaryAuthorId = mysqlCur.fetchone()
            if primaryAuthorId != None and primaryAuthorId[0] != None:
                writers.append(primaryAuthorId[0])

        # Try to match co authors
        if row[7] != None:
            coAuthors = row[7].split(' and ')
            for author in coAuthors:
                mysqlCur.execute("SELECT AuthorId FROM Author WHERE Name = %s", [author]) # Could try to use fuzzy matching for abbreviations
                authorId = mysqlCur.fetchone()
                if authorId != None and authorId[0] != None and authorId[0] not in writers:
                    writers.append(authorId[0])
        try:
            graphConn.insert_new_article(articleId, title, writers)
        except:
            pass

    print("FINISHED!")
    finalSeconds = time.time()
    print("Seconds to run: " + str(finalSeconds - seconds))


def insertCitationRelations(mysqlConn, graphConn):
    seconds = time.time()
    mysqlCur = mysqlConn.cursor()
    mysqlCur.execute("SELECT * FROM Citation")
    results = mysqlCur.fetchall()
    innerCur = mysqlConn.cursor()
    for row in results:
        print(row)
        articleId = row[0]
        sourceId = row[1]

        # Insert first article and primary author
        try:
            innerCur.execute("SELECT Title, PrimaryAuthorId FROM Article WHERE articleId = %s", [articleId])
            articleInfo = innerCur.fetchone()
            innerCur.execute("SELECT Name FROM Author WHERE authorId = %s", [articleInfo[1]])
            authorName = innerCur.fetchone()[0]
            graphConn.insert_new_author(articleInfo[1], authorName)
            graphConn.insert_new_article(articleId, articleInfo[0], [articleInfo[1]])
        except:
            pass
        # Insert second article and primary author
        try:
            innerCur.execute("SELECT Title, PrimaryAuthorId FROM Article WHERE articleId = %s", [sourceId])
            articleInfo = innerCur.fetchone()
            innerCur.execute("SELECT Name FROM Author WHERE authorId = %s", [articleInfo[1]])
            authorName = innerCur.fetchone()[0]
            graphConn.insert_new_author(articleInfo[1], authorName)
            graphConn.insert_new_article(sourceId, articleInfo[0], [articleInfo[1]])
        except:
            pass

        graphConn.insert_citation_relation(articleId, sourceId)
     
    print("FINISHED!")
    finalSeconds = time.time()
    print("Seconds to run: " + str(finalSeconds - seconds))

liteConn = sqlite3.connect("/Users/michaelvdow/Documents/CS 411/google-scholar.db")
liteConn.row_factory = sqlite3.Row
graphConn = graph_driver.Neo4jConnector()
mysqlConn = pymysql.connect(host='localhost',
                            user='root',
                            password='password',
                            db='googleScholar',
                            cursorclass = pymysql.cursors.SSCursor)

# Uncomment functions below to insert entries

# insertAuthors(mysqlConn, graphConn)
# insertWroteRelations(liteConn, mysqlConn, graphConn)
insertCitationRelations(mysqlConn, graphConn)