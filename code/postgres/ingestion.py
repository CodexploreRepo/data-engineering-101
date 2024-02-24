import os
import subprocess
from subprocess import PIPE

import pandas as pd
from sqlalchemy import Engine, create_engine


class DbConnector(object):
    def __init__(
        self,
        type: str,
        name: str,
        user: str,
        pw: str,
        port: str,
    ) -> None:
        self.type = type.lower()
        self.name = name
        self.user = user
        self.pw = pw
        self.port = port

    def get_engine(self) -> Engine:
        return create_engine(self.get_conn_uri())

    def get_conn_uri(self) -> str:
        # "postgresql://root:root@localhost:5432/nytaxi"
        return f"{self.type}://{self.user}:{self.pw}@localhost:{self.port}/{self.name}"


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
        self._remove(file_name)

        return df

    def write_to_db(self, df: pd.DataFrame, con: Engine) -> None:

        df.to_sql(name=self.table, con=con, if_exists="append")
