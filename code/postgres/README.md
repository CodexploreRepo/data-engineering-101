# NY Taxi

## Get Started

- Rename `.env_dev` to `.env` & fill in the `DB_USERNAME` & `DB_PASSWORD`
- `docker compose up -d` to bring up the Postgres DB container
- Access the Postgres via TablePlus or PgAdmin
- `sqlalchemy` python library to work with SQL
  - `psycopg2` sqlalchemy needs psycopg2 as it is a postgres db adapter for python
- Dataset: [NYC Taxi](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Pytest

- `cd` to the `postgres` directory and run `pytest`
