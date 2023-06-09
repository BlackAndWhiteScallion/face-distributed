import psycopg2

conn = psycopg2.connect("dbname = 'pyapp' user='student' password='student'")
cur = conn.cursor()
cur.execute("""
    TRUNCATE TABLE data 
""")
conn.commit();
