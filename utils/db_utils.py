from tinydb import TinyDB, Query
from pydantic import BaseModel
from typing import Type, TypeVar, Generic
from datetime import datetime

# Initialize TinyDB instance
db = TinyDB("db.json")

T = TypeVar("T", bound=BaseModel)


def query_translate(mongo_query):
    User = Query()

    def build_condition(q):
        if not isinstance(q, dict):
            raise ValueError("Query must be a dictionary")

        conditions = []

        for field, condition in q.items():
            if isinstance(condition, dict):
                # Operators inside
                for op, value in condition.items():
                    if op == "$eq":
                        conditions.append(getattr(User, field) == value)
                    elif op == "$ne":
                        conditions.append(getattr(User, field) != value)
                    elif op == "$gt":
                        conditions.append(getattr(User, field) > value)
                    elif op == "$gte":
                        conditions.append(getattr(User, field) >= value)
                    elif op == "$lt":
                        conditions.append(getattr(User, field) < value)
                    elif op == "$lte":
                        conditions.append(getattr(User, field) <= value)
                    elif op == "$in":
                        conditions.append(getattr(User, field).one_of(value))
                    elif op == "$nin":
                        conditions.append(~getattr(User, field).one_of(value))
                    else:
                        raise NotImplementedError(f"Unsupported operator: {op}")
            else:
                # Direct equality
                conditions.append(getattr(User, field) == condition)

        # Combine all conditions with AND
        from functools import reduce
        from operator import and_

        return reduce(and_, conditions)

    return build_condition(mongo_query)


class DBUtils(Generic[T]):
    @staticmethod
    def create(model: BaseModel):
        """Insert a Pydantic model object into the database."""
        table_name = model.__class__.__name__
        table = db.table(table_name)
        # Serialize datetime fields to ISO format
        serialized_data = model.model_dump()
        for key, value in serialized_data.items():
            if isinstance(value, datetime):
                serialized_data[key] = value.isoformat()
        table.insert(serialized_data)

    @staticmethod
    def update(model_class: Type[BaseModel], filters: dict, data: dict):
        """Update records in the database based on filters."""
        table_name = model_class.__name__
        table = db.table(table_name)
        query = Query()
        for key, value in filters.items():
            query = query & (getattr(Query(), key) == value)
        table.update(data, query)

    @staticmethod
    def find(model_class: Type[T], filters: dict) -> list[T]:
        """Find records in the database based on filters."""
        table_name = model_class.__name__
        table = db.table(table_name)

        if not filters:
            raise ValueError("Filters cannot be empty")

        q2 = query_translate(filters)
        # Execute the search and log the results
        results = table.search(q2)
        print(f"Debug: search results={results}")

        return [model_class(**item) for item in results]

    @staticmethod
    def delete(model_class: Type[BaseModel], filters: dict):
        """Delete records in the database based on filters."""
        table_name = model_class.__name__
        table = db.table(table_name)
        query = Query()
        for key, value in filters.items():
            query = query & (getattr(Query(), key) == value)
        table.remove(query)
