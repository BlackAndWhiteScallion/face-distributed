import psycopg2

conn = psycopg2.connect("dbname = 'pyapp' user='student' password='student'")
cur = conn.cursor()
cur.execute("""
        CREATE TABLE data(
            workerID int,
            videoID varchar(100),
            sendTime int,
            receiveTime int,
            frameNumber int
            );    
""")
conn.commit();
