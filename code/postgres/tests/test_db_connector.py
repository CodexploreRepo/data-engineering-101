from sqlalchemy.engine.base import Connection


def test_db_connector(c_postgres_connector):
    assert (
        c_postgres_connector.get_conn_uri()
        == "postgresql://root:root@localhost:5432/nytaxi"
    )
    # to check if the .connect() methods of the engine returns Connection object
    with c_postgres_connector.get_engine().connect() as connection:
        assert isinstance(connection, Connection)
