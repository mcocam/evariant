import os
import env # Environment variables
from sqlalchemy import create_engine, Engine, text


def get_connection() -> Engine:

    user: str = os.environ["DB_USER"]
    password: str = os.environ["DB_PASS"]
    database: str = os.environ["DB_DB"]


    connection: Engine = create_engine(f"mysql+pymysql://{user}:{password}@db:3306/{database}")

    return connection

