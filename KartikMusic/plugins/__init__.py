#
# Copyright (C) 2025-present by TheAloneTeam@Github, < https://github.com/TheAloneTeam >.
#
# This file is part of < https://github.com/TheAloneTeam/KartikMusic > project,
# and is released under the "MIT License".
# Please see < https://github.com/TheAloneTeam/KartikMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from pathlib import Path


def _list_modules():
    """
    List all Python module filenames (without extension) in the current directory,
    excluding the __init__.py file.

    Returns:
        list: A list of module names as strings.
    """
    mod_dir = Path(__file__).parent
    return [
        file.stem
        for file in mod_dir.glob("*.py")
        if file.is_file() and file.name != "__init__.py"
    ]


all_modules = frozenset(sorted(_list_modules()))
