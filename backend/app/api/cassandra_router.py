from fastapi import APIRouter
from app.lib.con_cass import cass_conn

router = APIRouter(prefix="/cassandra", tags=["Cassandra"])

@router.get("/data")
async def get_cassandra_data():
    # Example query
    result = cass_conn.execute_query("SELECT * FROM keyspace.table")
    return {"data": result}
