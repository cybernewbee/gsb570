import dbconnection

def view_my_data(conn):
    try:
        cur = conn.cursor()

        # SQL statement to delete rows where username is 'bob'
        sql = f"SELECT textattribute1, textattribute2, textattribute3, textattribute4, textattribute5 FROM public.rag WHERE username = 'dkraker@calpoly.edu'"
    
        # Execute the SQL statement
        cur.execute(sql)
        rows = cur.fetchall()

        # grab the cosine scores so we can compute Z score for narrow article selection
        for row in rows:
            print(row[0], row[1], row[2], row[3], row[4])
    
        

        
    except psycopg2.Error as e:
            print("An error occurred:", e)
    finally:
        if conn:
            conn.close()

    
conn = dbconnection.open_connection_to_db()
dbconnection.test_connection(conn)
view_my_data(conn)
