def translate_query(user_text: str) -> dict:
    """
    Dummy translator — in real usage, this would use OpenAI or Llama.
    """
    user_text = user_text.lower()
    if "kill" in user_text:
        return {"filter": {"event": "kill"}}
    return {"filter": {"event": "unknown"}}
