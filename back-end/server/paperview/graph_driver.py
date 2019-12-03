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

    def insert_citation_relation(self, ArticleId, SourceId):
        with self._driver.session() as session:
            session.write_transaction(self._create_cites_relation,
                                        ArticleId, SourceId)

    def insert_new_article_with_citations(self, ArticleId, Title, writers, citations):
        self.insert_new_article(ArticleId, Title, writers)

        with self._driver.session() as session:
            for source in citations:
                session.write_transaction(self._create_cites_relation,
                                          ArticleId, source)

    def delete_author(self, AuthorId):
        with self._driver.session() as session:
            session.write_transaction(self._delete_author_query, AuthorId)

    def delete_article(self, ArticleId):
        with self._driver.session() as session:
            session.write_transaction(self._delete_article_query, ArticleId)


    def update_author_name(self, AuthorId, new_name):
        with self._driver.session() as session:
            session.write_transaction(self._update_author_name_query,
                                      AuthorId, new_name)

    def update_article_title(self, ArticleId, new_title):
        with self._driver.session() as session:
            session.write_transaction(self._update_article_title_query,
                                      ArticleId, new_title)


    #def update_relations(self, Wrote, Cites):
    #    with self._driver.session() as session:
    #        session.write_transaction(self._update_article_title_query,
    #                                  ArticleId, new_title)

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

    @staticmethod
    def _create_cites_relation(tx, CitedBy, Source):
        result = tx.run("MATCH (citer:Article {ArticleId: $CitedBy}) "
                        "MATCH (source:Article {ArticleId: $Source}) "
                        "CREATE (citer)-[:Cites]->(source)",
                        CitedBy=CitedBy, Source=Source)

    @staticmethod
    def _delete_author_query(tx, AuthorId):
        result = tx.run("MATCH (deletedAuthor:Author {AuthorId: $AuthorId}) "
                        "DETACH DELETE deletedAuthor",
                        AuthorId=AuthorId)

    @staticmethod
    def _delete_article_query(tx, ArticleId):
        result = tx.run("MATCH (deletedArticle:Article {ArticleId: $ArticleId}) "
                        "DETACH DELETE deletedArticle",
                        ArticleId=ArticleId)

    @staticmethod
    def _update_author_name_query(tx, AuthorId, new_name):
        result = tx.run("MATCH (a:Author {AuthorId: $AuthorId}) "
                        "SET a.Name = $Name",
                        AuthorId=AuthorId, Name=new_name)

    @staticmethod
    def _update_article_title_query(tx, ArticleId, new_title):
        result = tx.run("MATCH (a:Article {ArticleId: $ArticleId}) "
                        "SET a.Title = $Title",
                        ArticleId=ArticleId, Title=new_title)

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
