from sqlalchemy import create_engine, text

DB_NAME = "music_api"
DB_USER = "postgres"
DB_PASSWORD = "my_password"
DB_HOST = "localhost"
DB_PORT = 5432

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

def init_database():
    engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": DB_NAME},
        )
        if result.fetchone():
            print(f"Database '{DB_NAME}' already exists.")
        else:
            connection.execute(text(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER}"))
            print(f"Database '{DB_NAME}' created successfully!")

if __name__ == "__main__":
    init_database()
