import mysql.connector
from dotenv import load_dotenv
import os
from contextlib import contextmanager
from fastapi import HTTPException
from mysql.connector import connect, Error
from typing import Any, Callable

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

def getDbConnection():
    return mysql.connector.connect(

        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USERNAME"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME"),

    )



@contextmanager
def db_connection():
    """Context manager to handle database connections."""
    connection = getDbConnection()
    try:
        yield connection
    finally:
        if connection.is_connected():
            connection.close()
