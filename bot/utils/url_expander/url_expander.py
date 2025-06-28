import urllib.request

def expand_url(short_url: str) -> str | None:
    """
    Expands a shortened URL to show its final destination.

    Args:
        `short_url`: The shortened URL to expand.

    Returns:
        `str|None`: The expanded URL if successful, `None` otherwise.
    """
    try:
        expanded_url = None
        response = urllib.request.urlopen(short_url)
        expanded_url = response.geturl()
    except Exception as e:
        pass
    finally:
        return expanded_url