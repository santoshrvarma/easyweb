from flask import abort
import psycopg2
from config import config

class Database:


    def display_swimmers(self):
        """ query data from the vendors table """
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT id,firstname, lastname, userid from regswimmer;")
            print("The number of swimmer: ", cur.rowcount)
            row = cur.fetchall()

            for x in row:
                print(x)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()