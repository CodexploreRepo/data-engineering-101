import os

import pytest
from ingestion import BaseIngestion


@pytest.mark.parametrize(
    "url",
    [
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-11.parquet"
    ],
)
class TestNytaxiIngestion:
    def test_download_function(
        self, c_nytaxi_ingestion: BaseIngestion, url: str
    ):
        file_name = c_nytaxi_ingestion._get_filename(url)
        c_nytaxi_ingestion._download(url, file_name)
        assert os.path.exists(file_name) is True

    def test_remove_function(self, c_nytaxi_ingestion: BaseIngestion, url: str):
        file_name = c_nytaxi_ingestion._get_filename(url)
        c_nytaxi_ingestion._remove(file_name)
        assert (not os.path.exists(file_name)) is True
