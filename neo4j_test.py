from neo4j import GraphDatabase, Auth


#Defines a class that interacts with the database
class Neo4j:
    #Constructor For Neo4j Database Connection
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    #Function for cypher query
    def query(self, query, age, database):
        connection = self.driver.session()
        results, summary, keys = self.driver.execute_query(query, age, database)
        return results

    #Function to close connection
    def disconnect(self):
        self.driver.close()

#Testing Connection In Main
def main():
    print("Testing Neo4j")

    #Parameters for establishing a neo4j connection
    uri = "neo4j+s://29245e19.databases.neo4j.io"
    user = "neo4j"
    password = "q_yFQ9wZyf2HyhCWAQkGN8vvUQi4rbLYTRdJ9SO_upE"
    a = (user, password)

    #Testing Connection Here
    with GraphDatabase.driver(uri, auth = a) as driver:
        driver.verify_connectivity()

    connection = Neo4j(uri, user, password)

    #Cypher Query
    query = """
    MATCH (p:Person {age: $age}) RETURN p.name AS name
    """

    #Execute The Query
    results, summary, keys = connection.query(query, 44, "neo4j")

    #Print Results
    for person in range(results):
        print(person)

    #Summary Info
    print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(results),
        time=summary.result_available_after,
    ))

    #Close Connection
    connection.disconnect()

#Execute function main
if __name__ == '__main__':
    main()
