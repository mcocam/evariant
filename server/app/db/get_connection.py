import os
import env # Environment variables
from sqlalchemy import create_engine, Engine, text


def get_connection() -> Engine:
    """Opens a connection to the database

    Returns:
        Engine: The connection to the database
    """

    user: str = os.environ["DB_USER"]
    password: str = os.environ["DB_PASS"]
    database: str = os.environ["DB_DB"]


    connection: Engine = create_engine(f"mysql+pymysql://{user}:{password}@db:3306/{database}")

    return connection

