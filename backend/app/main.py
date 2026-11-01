import uvicorn
from app.api.cassandra_router import router as cassandra_router
from app.api.dgraph_router import router as dgraph_router
from app.api.mongodb_router import router as mongodb_router
from app.lib.con_cass import cass_conn
from app.lib.con_dgh import dgh_conn
from app.lib.con_mdb import mdb_conn
from app.lib.con_r2 import r2_conn
from app.logger import Logger
from app.utils.create_dgraph_query import create_dgraph_query
from fastapi import FastAPI

app = FastAPI(title="FAKE PINTEREST API")

log = Logger.Logger()

# Include routers
app.include_router(mongodb_router)
app.include_router(cassandra_router)
app.include_router(dgraph_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    # Check MongoDB
    mdb_status = "OK"
    try:
        mdb_conn.client.admin.command('ping')
    except Exception as e:
        mdb_status = f"Disconnected or Error: {str(e)}"
    log.info(f"MongoDB Health Check: {mdb_status}")

    # Check Cassandra
    cass_status = "OK"
    try:
        cass_conn.session.execute("SELECT now() FROM system.local")
    except Exception as e:
        cass_status = f"Disconnected or Error: {str(e)}"
    log.info(f"Cassandra Health Check: {cass_status}")

    # Check Dgraph
    dgh_status = "OK"
    try:
        health_query = create_dgraph_query(
            query_name="health",
            queryfunc='has(name)',
            attributes=["uid"]
        )
        dgh_conn.execute_query(health_query)
    except Exception as e:
        dgh_status = f"Disconnected or Error: {str(e)}"
    log.info(f"Dgraph Health Check: {dgh_status}")

    r2_status = "OK"
    try:
        if r2_conn:
            r2_conn.s3_client.list_buckets()
        else:
            r2_status = "Not Initialized"
    except Exception as e:
        r2_status = f"Disconnected or Error: {str(e)}"
    log.info(f"R2 Health Check: {r2_status}")

    return {
        "mongodb": mdb_status,
        "cassandra": cass_status,
        "dgraph": dgh_status,
        "r2": r2_status
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
