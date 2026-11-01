"""
Formater because I hate to write queries by hand
"""
from typing import Optional

def create_dgraph_query(query_name: str,
                        queryfunc: str,
                        attributes: list[str],
                        directives: Optional[list[str]] = None) -> str:
    if directives is None:
        directives = []
    if attributes is None:
        attributes = []
    func_str = f"{query_name}(func: {queryfunc} ) "
    func_directives = " ".join(directives)
    attr_str = " ".join(attributes)
    query = f"""{{  {func_str} {func_directives} {{ {attr_str} }}}} """
    return query