import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        dbname='per_guilia', 
        user='postgres', 
        password='admin', 
        host='localhost',
        port=5432
    )

def get_reports():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM user_reports")
    reports = cur.fetchall()
    cur.close()
    conn.close()
    return reports

def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # Assuming the table name is 'moderators' and it has a column 'password_hash'
    cur.execute("SELECT * FROM moderators WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user
