# NY Taxi

## Get Started

- Rename `.env_dev` to `.env` & fill in the `DB_USERNAME` & `DB_PASSWORD`
- `docker compose up -d` to bring up the Postgres DB container
- Access the Postgres via TablePlus or PgAdmin
- `sqlalchemy` python library to work with SQL
  - `psycopg2` sqlalchemy needs psycopg2 as it is a postgres db adapter for python
- Dataset: [NYC Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Run

- `cd` to the main folder which contains the `docker-compose.yaml`
- Run the postgres service: `docker compose up -d nytaxi_db`
- Run the sql ingestion service: `docker compose up sql_ingestor`
  - If make the code change, need to re-build the image: `docker compose build`
- Once done, `docker-compose down` to remove all the service

## Pytest

- Run the postgres service: `docker compose up -d nytaxi_db`
- Activate conda env: `conda activate data_eng`
- `cd` to the `code/postgres` directory and run `pytest`
