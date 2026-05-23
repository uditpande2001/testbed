from storage.relational_db.postgres_client import (
    get_postgres_connection
)


def get_data():

    db = None
    cursor = None

    try:

        print("Connecting to database...")

        db = get_postgres_connection()

        cursor = db.cursor()

        query = """
            SELECT *
            FROM meter_mapping;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        print(results)

    except Exception as error:

        print(error)

    finally:

        if cursor is not None:
            cursor.close()

        if db is not None:
            db.close()

        print("Database connection closed")


if __name__ == '__main__':
    get_data()