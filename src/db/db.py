# Responsible for db modifications
import psycopg2
from constants import CONSTANTS


def init_database():
    # Connect to the specific database
    connection = psycopg2.connect(
        host=CONSTANTS["postgres_host"],
        user=CONSTANTS["postgres_user"],
        password=CONSTANTS["postgres_password"],
        dbname=CONSTANTS["postgres_db"],
    )
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs(
            id text PRIMARY KEY,
            link VARCHAR(255),
            title VARCHAR(255),
            company VARCHAR(255),
            date_posted VARCHAR(255),
            location VARCHAR(255),
            description text,
            timestamp timestamp DEFAULT current_timestamp
        );
        """
    )
    # Create the trigger function
    cursor.execute(
        f"""
        CREATE OR REPLACE FUNCTION delete_old_rows()
        RETURNS TRIGGER AS $$
        BEGIN
            DELETE FROM jobs WHERE timestamp < NOW() - INTERVAL '{CONSTANTS["deletion_interval"]}';
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    cursor.execute(
        f"""
        CREATE OR REPLACE TRIGGER delete_old_rows_trigger
        AFTER INSERT ON jobs
        EXECUTE FUNCTION delete_old_rows();
        """
    )

    connection.commit()
    cursor.close()
    connection.close()


def insert(data_tuple):
    connection = psycopg2.connect(
        host=CONSTANTS["postgres_host"],
        user=CONSTANTS["postgres_user"],
        password=CONSTANTS["postgres_password"],
        dbname=CONSTANTS["postgres_db"],
    )
    cur = connection.cursor()

    insert_statement = """
        INSERT INTO jobs (id, link, title, company, date_posted, location, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """

    try:
        cur.execute(insert_statement, data_tuple)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cur.close()
        connection.close()
