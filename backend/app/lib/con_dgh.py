import os
import pydgraph
import json


class DgraphConnection:
    def __init__(self):
        host = os.getenv("DGRAPH_HOST", "dgraph:9080")
        conn_str = f"dgraph://{host}"
        self.client = pydgraph.open(conn_str)

    def execute_mutation(self, mutation):
        txn = self.client.txn()
        try:
            res = txn.mutate(mutation)
            txn.commit()
            return res
        finally:
            txn.discard()

    def execute_query(self, query: str):
        txn = self.client.txn(read_only=True)
        try:
            res = txn.query(query)
            if hasattr(res, 'json'):
                return res.json
            elif isinstance(res, bytes):
                return json.loads(res.decode('utf-8'))
            return res
        finally:
            txn.discard()
        

# Initialize a singleton instance
dgh_conn = DgraphConnection()
