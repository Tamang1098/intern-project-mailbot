def get_category(subject, body):
    text = (subject + " " + body).lower()

    if any(w in text for w in ["payment", "invoice", "bill", "refund"]):
        return "billing"

    elif any(w in text for w in ["order", "buy", "price", "shipping"]):
        return "sales"

    elif any(w in text for w in ["error", "issue", "login", "blocked", "help"]):
        return "support"

    return None