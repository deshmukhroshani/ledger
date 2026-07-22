import psycopg2

def fetch_from_cloud_sql(table_name):
    conn = psycopg2.connect(
        host='34.74.95.159',
        user='postgres',
        password='Ledger@2025',
        dbname='ledger-core-db'
    )
    cursor = conn.cursor()
    sql = f"SELECT * FROM {table_name}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows