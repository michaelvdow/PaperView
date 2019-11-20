from neo4j import GraphDatabase

URI = 'bolt://localhost:7687/'
USER = 'neo4j'
PASSWORD = 'testpassword'

class Neo4jConnector(object):
    def __init__(self):
        self._driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def close(self):
        self._driver.close()


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
