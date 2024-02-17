def test_db_connector(c_postgres_connector):
    assert (
        c_postgres_connector.get_conn_uri()
        == "postgresql://root:root@localhost:5432/nytaxi"
    )
