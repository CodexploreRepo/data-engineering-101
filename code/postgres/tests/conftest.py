import os

import pytest
from dotenv import find_dotenv, load_dotenv
from ingestion import BaseIngestion

load_dotenv(find_dotenv())


@pytest.fixture()
def c_nytaxi_ingestion():
    return BaseIngestion(table=os.environ["DB_NAME"])
