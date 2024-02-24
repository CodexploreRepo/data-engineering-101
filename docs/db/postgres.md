# Postgres

## Introduction

- `$PGDATA=/var/lib/postgresql/data` is mapped to the volume folder of the docker container

```bash
docker exec -ti nytaxi_db_cont bash
root@5192aa33bf01:/# ls $PGDATA
base	      pg_dynshmem    pg_logical    pg_replslot	 pg_stat      pg_tblspc    pg_wal		 postgresql.conf
global	      pg_hba.conf    pg_multixact  pg_serial	 pg_stat_tmp  pg_twophase  pg_xact		 postmaster.opts
pg_commit_ts  pg_ident.conf  pg_notify	   pg_snapshots  pg_subtrans  PG_VERSION   postgresql.auto.conf  postmaster.pid
```

- Postgres `postgresql.conf` file:

  - Check the `postgresql.conf` file's location: access `psql` and run the command `SHOW config_file;`

    ```bash
    psql=: SHOW config_file;
    #              config_file
    #------------------------------------------
    # /var/lib/postgresql/data/postgresql.conf
    ```

    - To read `postgresql.conf` file:

    ```bash
    cat $PGDATA/postgresql.conf | grep max_wal_size
    max_wal_size = 1GB
    ```

- `pg_wal` is the subdirectory of the main PostgreSQL data directory where WAL files are stored.
  - Usually the `max_wal_size = 1GB` defined in the `postgresql.conf` file

## Postgres Access with `sqlalchemy`

- `sqlalchemy`: python library to work with SQL
  - `psycopg2`: sqlalchemy needs psycopg2 as it is a postgres_db adapter for python

### `sqlalchemy`

#### Engine

- The typical usage of `sqlalchemy.create_engine()` is once per particular database URL, held globally for the lifetime of a single application process
  - MYSQL `engine = create_engine("mysql+mysqldb://scott:tiger@localhost/db_name")`
  - Postgres `engine = create_engine("postgresql+psycopg2://user:password@ip:port/db_name")`
- `Engine` manages many individual **DBAPI** connections on behalf of the process and is intended to be called upon in a concurrent fashion.
- The `Engine` is not synonymous to the **DBAPI** `connect()` function, which represents just one connection resource

#### Connection

- `Engine.connect()` method returns a `Connection` object, and by using it in a Python context manager (e.g. the with: statement)
  - `Connection.close()` method is automatically invoked at the end of the block.
  - `Connection` is a proxy object for an actual DBAPI connection.
- To invoke the textual SQL statement, using `sqlalchemy.text()` to wrap the query string

```python
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(
        # using text() of sqlalchemy to convert string to SQL syntax
        text(
            """
            DROP TABLE IF EXISTS yellow_taxi;
            """
            )
        )
    conn.commit()
```

#### Pandas

- Infer the schema: `pd.io.sql.get_schema(df, name="yellow_taxi", con=engine)`
- Write to DB:

```Python
# to create the table
df.head(n=0).to_sql(name='yellow_taxi', con=engine, if_exists='replace')
# to append the data to the table
df.to_sql(name='yellow_taxi',
          con=engine,
          if_exists='append',
          index=False # this to prevent insert the index into the  database
) # to append the data to the database
```

- To read from DB:

```Python
import pandas as pd
pd.read_sql("SELECT * FROM yellow_taxi;", con=engine).head(5)

pd.read_sql("SELECT COUNT(*) AS cur_record FROM yellow_taxi;", con=engine)

# to check tables available in DB
query = """
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND
      schemaname != 'information_schema';
"""
pd.read_sql(query, con=engine)
```

## `psql` CLI

- To access nytaxi via CLI: `docker exec -ti nytaxi_db_cont psql -U root -d nytaxi`

```shell
docker exec -ti nytaxi_db_cont psql -U root -d nytaxi

# psql (16.1 (Debian 16.1-1.pgdg120+1))
nytaxi=# \dt # \dt to list the tables
# List of relations
#  Schema |       Name       | Type  | Owner
# --------+------------------+-------+-------
#  public | yellow_taxi_data | table | root

nytaxi-# \d yellow_taxi_data # to get the table description
#                            Table "public.yellow_taxi_data"
#         Column         |            Type             | Collation | Nullable | Default
# -----------------------+-----------------------------+-----------+----------+---------
#  index                 | bigint                      |           |          |
#  VendorID              | integer                     |           |          |
#  tpep_pickup_datetime  | timestamp without time zone |           |          |
#  tpep_dropoff_datetime | timestamp without time zone |           |          |
#  passenger_count       | double precision            |           |          |
# Indexes:
#     "ix_yellow_taxi_data_index" btree (index)
```
