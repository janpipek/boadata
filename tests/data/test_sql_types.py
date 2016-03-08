from boadata.data.sql_types import DatabaseTable


class TestAcceptsUri:
    def test_schema_uri(self):
        valid_uris = [
            "postgresql://hostname::tablename",
            "sqlite:///relative/path/to/myfile.db::tablename",
            "sqlite:////absolute/path/to/myfile.db::tablename",
        ]

        invalid_urls = [
            "unknown://schema::tablename",
            "no::schema_no_file"
            "sqlite:////absolute/path/to/myfile.db::",
            "sqlite:////absolute/path/to/myfile.db",
        ]

        for uri in valid_uris:
            assert DatabaseTable.accepts_uri(uri)

        for uri in invalid_urls:
            assert not DatabaseTable.accepts_uri(uri)

    def test_sqlite_file_uris(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db") as named:
            assert DatabaseTable.accepts_uri(named.name)


if __name__ == "__main__":
    import pytest
    pytest.main(__file__)