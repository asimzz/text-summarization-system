import os
from pymongo import MongoClient
from pymongo.database import Database, Collection
from loguru import logger

def connect_to_mongo():
    """
    This function establishes a connection to the MongoDB database using the URL
    provided in the environment variable 'MONGO_DB_URL'.
    Returns:
        Database: The MongoDB database object.
    Raises:
        Exception: If there is an error connecting to the MongoDB database.
    """
    client = MongoClient(os.getenv("MONGO_DB_URL"))
    database = client["development"]

    try:
        client.admin.command("ping")
        logger.success("### Database is Connected Successfully! ###")
    except Exception as e:
        raise Exception("The following error occurred: ", e)
    
    return database


def get_collection(database: Database, collection_name: str) -> Collection:
    """
    This function retrieves a collection from the specified database.
    Args:
        database (Database): The database object.
        collection_name (str): The name of the collection to retrieve.
    Returns:
        Collection: The collection object.
    """
    collection = database[f"{collection_name}"]
    return collection
