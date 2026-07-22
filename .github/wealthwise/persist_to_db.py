import psycopg2

def persist_to_cloud_sql(data, table_name):
    conn = psycopg2.connect(
        host='34.74.95.159',
        user='postgres',
        password='Ledger@2025',
        dbname='ledger-core-db'
    )
    cursor = conn.cursor()
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(data.values()))
    conn.commit()
    cursor.close()
    conn.close()