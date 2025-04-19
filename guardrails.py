def check_safety_guardrails(user_query: str) -> str:
    """
    Guardrails to check for unsafe, sensitive, or unrelated queries
    Returns a reason string if blocked, otherwise returns empty string
    """
    blocked_keywords = [
        "kill", "bomb", "attack", "hack", "bypass", "shutdown",
        "sexual", "violence", "drugs", "weapon", "terror", "explode"
    ]
    normalized_query = user_query.lower()
    for keyword in blocked_keywords:
        if keyword in normalized_query:
            return f"Query blocked due to use of prohibited term: '{keyword}'"

    return ""  
