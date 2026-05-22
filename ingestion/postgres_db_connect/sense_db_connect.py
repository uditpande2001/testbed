import psycopg2

db = None
cursor = None

def get_data():
    try:
        print("\n", flush=True)
        print('connecting to database', flush=True)
        db = psycopg2.connect(
            host='216.48.180.61',
            database='sensedb',
            user='postgres',
            password='probus@220706'
        )
        cursor = db.cursor()
        query = f"""							
                                SELECT * 
                                FROM meter_mapping; 
                                
"""
        print("running query", flush=True)
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)


        db.close()


    except Exception as error:
        print(error, flush=True)
    finally:
        if cursor is not None:
            print("database connection closed", flush=True)
            print("\n", flush=True)

            cursor.close()
        if db is not None:
            db.close()


if __name__ == '__main__':
    get_data()