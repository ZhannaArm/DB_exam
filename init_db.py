import psycopg2

DB_NAME = "music_api"
DB_USER = "postgres"
DB_PASSWORD = "mysecretpassword"
DB_HOST = "localhost"
DB_PORT = 5432

def init_db():
    try:
        conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        conn.autocommit = True
        cursor = conn.cursor()


        cursor.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER};")
        print(f"Database {DB_NAME} created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    init_db()
