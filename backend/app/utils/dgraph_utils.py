"""
Formater because I hate to write queries by hand
"""
from __future__ import annotations
from typing import Optional
from enum import Enum


class DgraphIndexType(Enum):        
    # String index types    
    INDEX_TERM = "term"
    INDEX_EXACT = "exact"
    INDEX_FULLTEXT = "fulltext"
    INDEX_HASH = "hash"
    INDEX_TRIGRAM = "trigram"
    INDEX_NGRAM = "ngram"

    # Vector index type
    INDEX_HNSW = "hnsw"

    # Date index types
    INDEX_YEAR = "year"
    INDEX_MONTH = "month"
    INDEX_DAY = "day"
    INDEX_HOUR = "hour"

    # Scalar index types
    INDEX_INT = "int"
    INDEX_FLOAT = "float"
    INDEX_BOOL = "bool"
    INDEX_GEO = "geo"
    
class DgraphIndexFormat:
    def __init__(self, value: str, type_str: str, indexType: DgraphIndexType):
        self.value = value
        self.type_str = type_str
        self.indexType = indexType

    def __str__(self):
        return f"{self.value}: {self.type_str} @index({self.indexType.value}) ."

class DgraphTypeFormat:
    def __init__(self, type_name: str, value: list[str]):
        self.type_name = type_name
        self.value = value

    def __str__(self):
        return f"{self.value}: {self.type_name} ."

class DgraphRelationFormat:
    def __init__(self, name: str, values: list[str], relations: list[DgraphRelationFormat] | None = None):
        self.name = name
        self.values = values
        if relations is not None:
            if not isinstance(relations, list):
                raise TypeError(
                    f"Wrong argument type for relations. Expected list, but got {type(relations).__name__}."
                )
            for rel in relations:
                if not isinstance(rel, DgraphRelationFormat):
                    raise TypeError("All items inside 'relations' must be instances of DgraphRelationFormat.")
        self.relations = relations

    def __str__(self):
        relation_str = f"{self.name} {{ {' '.join(self.values)} }}"
        if self.relations:
            for relation in self.relations:
                relation_str += f" {relation!s}"
        return relation_str

class DgraphUtils:
    def create_dgraph_query(self,
                            query_name: str,
                            queryfunc: str,
                            attributes: list[str],
                            directives: Optional[list[str]] = None,
                            relations: Optional[list[DgraphRelationFormat]] = None) -> str:
        directives = directives or []
        attributes = attributes or []
        
        func_str = f"{query_name}(func: {queryfunc})"
        func_directives = " ".join(directives)
        header = f"{func_str} {func_directives}".strip()
        attr_str = " ".join(attributes)
        if relations:
            relation_str = " ".join(str(rel) for rel in relations)
            query = f"{{ {header} {{ {attr_str} {relation_str} }} }}"
        else:
            query = f"{{ {header} {{ {attr_str} }} }}"
        return query
    
    def create_schema(self,
                      schema_type_name: str,
                      values: list[str],
                      indexes: Optional[list[DgraphIndexFormat]] = None,
                      values_type: Optional[list[DgraphTypeFormat]] = None) -> str:
        indexes = indexes or []
        values = values or []
        values_type = values_type or []

        schema_lines = [
            f"type {schema_type_name} {{",    
        ]
        for value in values:
            schema_lines.append(f"    {value}")
        
        schema_lines.append("}\n")
        
        for idx in indexes:
            schema_lines.append(str(idx))
            
        for v_type in values_type:
            schema_lines.append(str(v_type))
        
        schema_lines.append("\n")
        
        return "\n".join(schema_lines)
