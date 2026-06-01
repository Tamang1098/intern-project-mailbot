from database.db import get_connection

def get_receivers(category):
    if not category:
        return []

    category = category.lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT receiver_email FROM receivers WHERE category=%s",
        (category,)
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return [r[0] for r in results]