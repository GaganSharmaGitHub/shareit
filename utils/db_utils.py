from tinydb import TinyDB, Query
from pydantic import BaseModel
from typing import Type

# Initialize TinyDB instance
db = TinyDB("db.json")


class DBUtils:
    @staticmethod
    def create(model: BaseModel):
        """Insert a Pydantic model object into the database."""
        table_name = model.__class__.__name__
        table = db.table(table_name)
        table.insert(model.model_dump())

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
    def find(model_class: Type[BaseModel], filters: dict):
        """Find records in the database based on filters."""
        table_name = model_class.__name__
        table = db.table(table_name)
        query = Query()
        for key, value in filters.items():
            query = query & (getattr(Query(), key) == value)
        return table.search(query)

    @staticmethod
    def delete(model_class: Type[BaseModel], filters: dict):
        """Delete records in the database based on filters."""
        table_name = model_class.__name__
        table = db.table(table_name)
        query = Query()
        for key, value in filters.items():
            query = query & (getattr(Query(), key) == value)
        table.remove(query)
