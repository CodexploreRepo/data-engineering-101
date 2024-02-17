# NY Taxi

## Get Started

- Rename `.env_dev` to `.env` & fill in the `DB_USERNAME` & `DB_PASSWORD`
- `docker compose up -d` to bring up the Postgres DB container
- Access the Postgres via TablePlus or PgAdmin
- `sqlalchemy` python library to work with SQL
  - `psycopg2` sqlalchemy needs psycopg2 as it is a postgres db adapter for python
- Dataset: [NYC Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Postgres

- To access nytaxi via CLI: `docker exec -ti nytaxi_db_cont psql -U root nytaxi`

```shell
docker exec -ti nytaxi_db_cont psql -U root nytaxi

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
