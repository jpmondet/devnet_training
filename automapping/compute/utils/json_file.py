#! /usr/bin/env python3

from os import access, R_OK
from typing import List, Dict, Any
from json import load as jload
from json.decoder import JSONDecodeError


def _safe_load_json_file(filename: str):
    if not access(filename, R_OK):
        return None

    datas: List[Dict[str, Any]] = None
    try:
        with open(filename, "r") as fp:
            datas = jload(fp)
    except JSONDecodeError:
        return None

    return datas
