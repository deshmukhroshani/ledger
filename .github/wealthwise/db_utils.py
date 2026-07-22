# db_utils.py
import psycopg2

def get_conn():
    return psycopg2.connect(
        host="34.74.95.159",
        port=5432,
        database="ledger-core-db",
        user="postgres",
        password="Ledger@2025"
    )

def insert_user(first_name, last_name, email, password, sex, country, dob):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_profile (first_name, last_name, email_address, password, sex, country, dob)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (first_name, last_name, email, password, sex, country, dob))
        conn.commit()
        return {"status": "success"}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return {"status": "error", "message": "Email already exists."}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()
