from string import ascii_lowercase


def transform_to_chapter_dir(stem: str):
    """
    Make chapter dir name from file name
    """
    _temp = stem
    _temp = _temp.lower().replace(" ", "-")
    _new_temp = ""
    for ch in _temp:
        if ch in ascii_lowercase + "-":
            _new_temp += ch
    return _new_temp
