def format_string(input_string: str) -> str:
    """Formats a string to have the first letter capitalized"""
    if not input_string:
        return ""
    return input_string.strip().capitalize()