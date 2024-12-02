import os
from datetime import datetime

# Dependency to provide the current year
def get_year():
    """Return the current year as a dictionary."""
    current_year = datetime.now().year
    return {"year": current_year}

def get_image_paths(image_dir: str, exclude_substr: list[str]=['orig', 'diela', 'tools.png', '.ico']):
    # List image file paths
    images = os.listdir(image_dir)
    cond = lambda img: not any(substr in img for substr in exclude_substr)
    image_paths = [f"/static/img/{img}" for img in images if cond(img)]
    return image_paths


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    import re
    import unicodedata
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
