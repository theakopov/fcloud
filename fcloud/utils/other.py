def generate_new_name(busy: list[str], default: str) -> str:
    """If the name under which they are trying
    to upload the file to the cloud is already
    taken, using this function, a new name
    will be generated

    Args:
        busy (list[str]): List of names already taken
        default (str): The name of the file to be changed

    Returns:
        str: New file name. For example 'film.mp4 (2)'.
    """
    i = 1
    while f"{default} ({i})" in busy:
        i += 1

    return f"{default} ({i})"
