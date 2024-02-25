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
    # def test_download_function(
    #     self, c_nytaxi_ingestion: BaseIngestion, url: str
    # ):
    #     file_name = c_nytaxi_ingestion._get_filename(url)
    #     c_nytaxi_ingestion._download(url, file_name)
    #     assert os.path.exists(file_name) is True

    # def test_remove_function(self, c_nytaxi_ingestion: BaseIngestion, url: str):
    #     file_name = c_nytaxi_ingestion._get_filename(url)
    #     c_nytaxi_ingestion._remove(file_name)
    #     assert (not os.path.exists(file_name)) is True

    def test_write_to_db(
        self,
        c_nytaxi_ingestion: BaseIngestion,
        url: str,
    ):
        df = c_nytaxi_ingestion.read(url)

        sample_size = 5
        table = "test_db"
        # ingest the data into the DB
        c_nytaxi_ingestion.write_to_db(df.head(sample_size), table)
        # compare the count with the sample size
        assert (
            c_nytaxi_ingestion.execute_sql(f"SELECT COUNT(*) FROM {table}")[0][
                0
            ]
            == sample_size
        )
        # once done, drop the table
        c_nytaxi_ingestion.execute_sql(f"DROP TABLE IF EXISTS {table}")
