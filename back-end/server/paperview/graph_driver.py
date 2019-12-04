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
            session.write_transaction(self._insert_author_query, AuthorId, Name)

    def insert_new_article(self, ArticleId, Title, writers):
        with self._driver.session() as session:
            session.write_transaction(self._insert_article_query, ArticleId, Title)
            for i in range(len(writers)):
                AuthorId = writers[i]
                session.write_transaction(self._create_wrote_relation,
                                          ArticleId, AuthorId, i)

    def insert_citation_relation(self, ArticleId, SourceId):
        with self._driver.session() as session:
            session.write_transaction(self._create_cites_relation, ArticleId, SourceId)

    def insert_new_article_with_citations(self, ArticleId, Title, writers,
                                          citations):
        self.insert_new_article(ArticleId, Title, writers)

        with self._driver.session() as session:
            for source in citations:
                session.write_transaction(self._create_cites_relation, ArticleId, source)

    def delete_author(self, AuthorId):
        with self._driver.session() as session:
            session.write_transaction(self._delete_author_query, AuthorId)

    def delete_article(self, ArticleId):
        with self._driver.session() as session:
            session.write_transaction(self._delete_article_query, ArticleId)


    def update_author_name(self, AuthorId, new_name):
        with self._driver.session() as session:
            session.write_transaction(self._update_author_name_query, AuthorId, new_name)

    def update_article_title(self, ArticleId, new_title):
        with self._driver.session() as session:
            session.write_transaction(self._update_article_title_query,
                                      ArticleId, new_title)

    def get_articles_written_by(self, AuthorId):
        with self._driver.session() as session:
            return session.read_transaction(self._get_written_articles_query, AuthorId)

    def get_authors_of(self, ArticleId):
        with self._driver.session() as session:
            return session.read_transaction(self._get_authors_of_query, ArticleId)

    # ID should be the ArticleId or AuthorId; node_type should be 'Article' or 'Author'
    def get_graph_data(self, ID, node_type):
        data = {}
        with self._driver.session() as session:
            data['nodes'] = session.read_transaction(self._get_nearby_nodes,
                                                     ID, node_type)
            data['edges'] = session.read_transaction(self._get_nearby_edges,
                                                     ID, node_type)
        return data

    @staticmethod
    def _create_id_constraints(tx):
        tx.run("CREATE CONSTRAINT ON (a:Author) ASSERT a.AuthorId IS UNIQUE")
        tx.run("CREATE CONSTRAINT ON (a:Article) ASSERT a.ArticleId IS UNIQUE")

    @staticmethod
    def _get_nearby_nodes(tx, ID, root_type):
        result = tx.run("MATCH (root) "
                        "WHERE ($root_type = 'Article' AND root.ArticleId = $ID) "
                        "    OR ($root_type = 'Author' AND root.AuthorId = $ID) "
                        "MATCH (root)-[*0..2]-(a) "
                        "WITH DISTINCT a "
                        "WITH LABELS(a)[0] AS type, a "
                        "RETURN type, "
                        "CASE type "
                        "    WHEN 'Article' THEN a.Title "
                        "    WHEN 'Author' THEN a.Name "
                        "END AS label, "
                        "CASE type "
                        "    WHEN 'Article' THEN a.ArticleId "
                        "    WHEN 'Author' THEN a.AuthorId "
                        "END AS linkId, "
                        "ID(a) as id",
                        root_type=root_type, ID=ID)
        nodes = []
        for record in result:
            nodes.append(
                {
                    'id': record['id'],
                    'type': record['type'],
                    'label': record['label'],
                    'linkId': record['linkId']
                }
            )
        return nodes

    @staticmethod
    def _get_nearby_edges(tx, ID, root_type):
        result = tx.run("MATCH (root) "
                        "WHERE ($root_type = 'Article' AND root.ArticleId = $ID) "
                        "    OR ($root_type = 'Author' AND root.AuthorId = $ID) "
                        "MATCH (root)-[*0..2]-()-[r]-()-[*0..2]-(root) "
                        "WITH DISTINCT r "
                        "RETURN type(r) AS type, "
                        "id(startNode(r)) AS from, id(endNode(r)) AS to",
                        root_type=root_type, ID=ID)
        edges = []
        for record in result:
            edges.append(
                {
                    'from': record['from'],
                    'to': record['to'],
                    'type': record['type']
                }
            )
        return edges

    @staticmethod
    def _get_written_articles_query(tx, AuthorId):
        result = tx.run("MATCH (:Author {AuthorId: $AuthorId})-[:Wrote]->(a:Article) "
                        "RETURN a.ArticleId, a.Title "
                        "ORDER BY a.Title",
                        AuthorId=AuthorId)
        article_list = []
        for record in result:
            article_list.append(
                {'ArticleId': record['a.ArticleId'], 'Title': record['a.Title']}
            )
        return article_list

    @staticmethod
    def _get_authors_of_query(tx, ArticleId):
        result = tx.run("MATCH (a:Author)-[w:Wrote]->(:Article {ArticleId: $ArticleId}) "
                        "RETURN a.AuthorId, a.Name "
                        "ORDER BY w.rank ",
                        ArticleId=ArticleId)
        author_list = []
        for record in result:
            author_list.append(
                {'AuthorId': record['a.AuthorId'], 'Name': record['a.Name']}
            )
        return author_list

    @staticmethod
    def _insert_author_query(tx, AuthorId, Name):
        tx.run("MERGE (a:Author {AuthorId: $AuthorId}) "
               "SET a.Name = $Name ",
               AuthorId=AuthorId, Name=Name)

    @staticmethod
    def _insert_article_query(tx, ArticleId, Title):
        tx.run("MERGE (a:Article {ArticleId: $ArticleId}) "
               "SET a.Title = $Title ",
               ArticleId=ArticleId, Title=Title)

    @staticmethod
    def _create_wrote_relation(tx, ArticleId, AuthorId, rank):
        tx.run("MATCH (art:Article {ArticleId: $ArticleId}) "
               "MATCH (wri:Author {AuthorId: $AuthorId}) "
               "CREATE (wri)-[:Wrote {rank: $rank}]->(art)",
               ArticleId=ArticleId, AuthorId=AuthorId, rank=rank)

    @staticmethod
    def _create_cites_relation(tx, CitedBy, Source):
        tx.run("MATCH (citer:Article {ArticleId: $CitedBy}) "
               "MATCH (source:Article {ArticleId: $Source}) "
               "CREATE (citer)-[:Cites]->(source)",
               CitedBy=CitedBy, Source=Source)

    @staticmethod
    def _delete_author_query(tx, AuthorId):
        tx.run("MATCH (deletedAuthor:Author {AuthorId: $AuthorId}) "
               "DETACH DELETE deletedAuthor",
               AuthorId=AuthorId)

    @staticmethod
    def _delete_article_query(tx, ArticleId):
        tx.run("MATCH (deletedArticle:Article {ArticleId: $ArticleId}) "
               "DETACH DELETE deletedArticle",
               ArticleId=ArticleId)

    @staticmethod
    def _update_author_name_query(tx, AuthorId, new_name):
        tx.run("MATCH (a:Author {AuthorId: $AuthorId}) "
               "SET a.Name = $Name",
               AuthorId=AuthorId, Name=new_name)

    @staticmethod
    def _update_article_title_query(tx, ArticleId, new_title):
        tx.run("MATCH (a:Article {ArticleId: $ArticleId}) "
               "SET a.Title = $Title",
               ArticleId=ArticleId, Title=new_title)

    ## Test methods


    def get_how_titles(self):
        with self._driver.session() as session:
            return session.read_transaction(self._get_how_titles_query)
            

    @staticmethod
    def _get_how_titles_query(tx):
        result = tx.run ("MATCH (a:Article) "
                         "WHERE a.Title STARTS WITH 'How' "
                         "RETURN a.Title")
        title_list = []
        for record in result:
            title_list.append(record['a.Title'])
        return title_list

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
