#! /usr/bin/env python3

from os import access, R_OK
from time import sleep
from typing import List, Dict, Any
from json.decoder import JSONDecodeError
from requests import get as rget
import requests.exceptions


class NetworkError(RuntimeError):
    pass


def _retryer(max_retries=10, timeout=5):
    def wraps(func):
        request_exceptions = (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.SSLError,
        )

        def inner(*args, **kwargs):
            for i in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                except request_exceptions:
                    sleep(timeout * i)
                    continue
                else:
                    return result
            else:
                raise NetworkError

        return inner

    return wraps


@_retryer()
def get_from_api(url: str) -> Dict[str, Any]:
    try:
        return rget(url).json()
    except JSONDecodeError:
        return {}