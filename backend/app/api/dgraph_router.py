from fastapi import APIRouter
from app.lib.con_dgh import dgh_conn
from typing import Any
from app.utils.dgraph_utils import DgraphUtils

router = APIRouter(prefix="/dgraph", tags=["Dgraph"])
dgh_u = DgraphUtils()

@router.get("/data")
async def get_dgraph_data():
    query = dgh_u.create_dgraph_query(
        query_name="q",
        queryfunc='eq(name, "test")',
        attributes=["uid", "name"]
    )
    try:
        result = dgh_conn.execute_query(query)
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}
