import os
from cassandra.cluster import Cluster

class CassandraConnection:
    def __init__(self):
        host = os.getenv("CASSANDRA_HOST", "cassandra")
        self.cluster = Cluster([host])
        self.session = self.cluster.connect()

    def execute_query(self, query):
        return self.session.execute(query)

# Initialize a singleton instance
cass_conn = CassandraConnection()
