#! /usr/bin/env python

from typing import List
from random import randint


def main() -> None:

    numbers: List[int] = [ randint(0,9) ] * 10000000

    for number in numbers:
        number = number ** 1000

if __name__ == '__main__':
    main()
