from neo4j import GraphDatabase

URI = 'bolt://localhost:7687/'
USER = 'neo4j'
PASSWORD = 'testpassword'

class Neo4jConnector(object):
    def __init__(self):
        self._driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        with self._driver.session() as session:
            session.write_transaction(self._create_id_constraints)

    def close(self):
        self._driver.close()

    def insert_new_author(self, AuthorId, Name):
        with self._driver.session() as session:
            return session.write_transaction(self._insert_author_query, AuthorId, Name)

    def insert_new_article(self, ArticleId, Title, writers):
        with self._driver.session() as session:
            session.write_transaction(self._insert_article_query,
                                             ArticleId, Title)
            for i in range(len(writers)):
                AuthorId = writers[i]
                session.write_transaction(self._create_wrote_relation,
                                          ArticleId, AuthorId, i)

    @staticmethod
    def _create_id_constraints(tx):
        tx.run("CREATE CONSTRAINT ON (a:Author) ASSERT a.AuthorId IS UNIQUE")
        tx.run("CREATE CONSTRAINT ON (a:Article) ASSERT a.ArticleId IS UNIQUE")

    @staticmethod
    def _insert_author_query(tx, AuthorId, Name):
        result = tx.run("CREATE (a:Author) "
                        "SET a.AuthorId = $AuthorId "
                        "SET a.Name = $Name ",
                        AuthorId=AuthorId, Name=Name)

    @staticmethod
    def _insert_article_query(tx, ArticleId, Title):
        result = tx.run("CREATE (a:Article) "
                        "SET a.ArticleId = $ArticleId "
                        "SET a.Title = $Title ",
                        ArticleId=ArticleId, Title=Title)

    @staticmethod
    def _create_wrote_relation(tx, ArticleId, AuthorId, rank):
        result = tx.run("MATCH (art:Article {ArticleId: $ArticleId}) "
                        "MATCH (wri:Author {AuthorId: $AuthorId}) "
                        "CREATE (wri)-[:Wrote {rank: $rank}]->(art)",
                        ArticleId=ArticleId, AuthorId=AuthorId, rank=rank)

    ## Test methods

    def return_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting,
                                                 message)
            return greeting

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting,
                                                 message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]
