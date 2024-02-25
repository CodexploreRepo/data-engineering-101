import os
import subprocess
from subprocess import PIPE

import pandas as pd
from logzero import logger
from sqlalchemy import Engine, create_engine, text


class DbConnector(object):
    def __init__(
        self,
        type: str,
        name: str,
        user: str,
        pw: str,
        port: str,
        host: str = "localhost",
    ) -> None:
        self.type = type.lower()
        self.name = name
        self.user = user
        self.pw = pw
        self.port = port
        self.host = host

    def get_engine(self) -> Engine:
        return create_engine(self.get_conn_uri())

    def get_conn_uri(self) -> str:
        # "postgresql+psycopg2://root:root@localhost:5432/nytaxi"
        return f"{self.type}://{self.user}:{self.pw}@{self.host}:{self.port}/{self.name}"


class BaseIngestion(object):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

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

    def write_to_db(
        self, df: pd.DataFrame, table: str, if_exists: str = "replace"
    ) -> None:
        df.to_sql(name=table, con=self.engine, if_exists=if_exists, index=False)

    def execute_sql(self, sql_command: str) -> any:
        with self.engine.connect() as conn:
            cursor = conn.execute(text(sql_command))
            conn.commit()
            return cursor if cursor.rowcount == -1 else cursor.fetchall()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--table", help="Table name to write/update")
    parser.add_argument("-u", "--url", help="URL data source")
    parser.add_argument(
        "-H", "--db_host", help="the DB HOST IP", default="localhost"
    )

    args = parser.parse_args()
    logger.info(f"Args: {vars(args)}")
    postgresql_engine = DbConnector(
        "postgresql",
        os.environ["DB_NAME"],
        os.environ["DB_USERNAME"],
        os.environ["DB_PASSWORD"],
        os.environ["DB_PORT"],
        args.db_host,
    ).get_engine()

    sql_ingestor = BaseIngestion(postgresql_engine)
    df = sql_ingestor.read(args.url)

    logger.info(df.head())
    sql_ingestor.write_to_db(df.head(100), args.table)
    # sql_ingestor.execute_sql(f"DROP TABLE IF EXISTS {args.table}")
    logger.info(f"Table {args.table} has been successfully updated")
