from database.db import get_connection

def save_email(sender, subject, body, category, forwarded_to, status="processed"):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO emails (sender_email, subject, body, category, status, forwarded_to)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (sender, subject, body, category, status, forwarded_to))
    conn.commit()

    cursor.close()
    conn.close()