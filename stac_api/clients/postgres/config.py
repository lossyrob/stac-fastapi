from pydantic import BaseSettings

class PostgresSettings(BaseSettings):
    """Postgres settings"""

    postgres_user: str
    postgres_pass: str
    postgres_host_reader: str
    postgres_host_writer: str
    postgres_port: str
    postgres_dbname: str

    class Config:
        """model config"""

        extra = "allow"
        env_file = ".env"

    @property
    def reader_connection_string(self):
        """Create reader psql connection string"""
        return f"postgresql://{self.postgres_user}:{self.postgres_pass}@{self.postgres_host_reader}:{self.postgres_port}/{self.postgres_dbname}"

    @property
    def writer_connection_string(self):
        """Create writer psql connection string"""
        return f"postgresql://{self.postgres_user}:{self.postgres_pass}@{self.postgres_host_writer}:{self.postgres_port}/{self.postgres_dbname}"
