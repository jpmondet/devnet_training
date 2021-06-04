# Mypy usage

## Imports

Usually, need to import `from typing import Dict, List, Any`  (Dict and List shouldn't be needed starting from python3.9)

## Typing a variable

`a: int = 1`

## Checking the code

`mypy --strict code.py`

## Improving speed (sometimes) with mypyc

`pip install mypy.mypyc`

`mypyc example.py`  (the code must be correctly typed)

This should generate a `example.so` module by leveraging `CPython`

Then, in another script, we just have to import the `.o` like any other module `import example`
