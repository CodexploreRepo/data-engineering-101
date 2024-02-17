import os
import subprocess
from subprocess import PIPE

import pandas as pd
from sqlalchemy import Engine, create_engine


class DbConnector(object):
    def __init__(
        self,
    ) -> None:
        # engine = create_engine("postgresql://root:root@localhost:5432/nytaxi")
        pass


class BaseIngestion(object):
    def __init__(self, table: str) -> None:
        self.table = table

    def _download(self, url: str, file_name: str) -> None:
        if not os.path.exists(file_name):
            subprocess.run(["curl", "-O", url], stdout=PIPE, stderr=PIPE)

    def _remove(self, file_name) -> None:
        if os.path.exists(file_name):
            subprocess.run(["rm", file_name], stdout=PIPE, stderr=PIPE)

    def _get_filename(self, url: str) -> str:
        return url.split("/")[-1]

    def read(self, url) -> pd.DataFrame:
        file_name = self._get_filename(url)

        self._download(url, file_name)
        df = pd.read_parquet(file_name)
        self._remove()

        return df

    def write_to_db(self, df: pd.DataFrame, con: Engine) -> None:
        df.to_sql(name=self.table, con=con, if_exists="append")
