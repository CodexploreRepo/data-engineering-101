import os

import pytest
from dotenv import find_dotenv, load_dotenv
from ingestion import BaseIngestion, DbConnector

load_dotenv(find_dotenv())


@pytest.fixture()
def c_nytaxi_ingestion():
    return BaseIngestion(table=os.environ["DB_NAME"])


@pytest.fixture()
def c_postgres_connector():
    return DbConnector(
        "postgresql",
        os.environ["DB_NAME"],
        os.environ["DB_USERNAME"],
        os.environ["DB_PASSWORD"],
        os.environ["DB_PORT"],
    )
