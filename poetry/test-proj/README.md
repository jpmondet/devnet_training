# Basic poetry usage


## Prep the env

`poetry new test_proj`

(or `poetry init` on an existing project)

## Add dependencies 

`poetry add requests`

## Install dependencies

`poetry install` (assuming pypi official repo)

(if the repo needs credential : `poetry config http-basic.foo username password` or other methods : https://python-poetry.org/docs/repositories/)

If private repo : 
`poetry config repositories.foo https://foo.bar/simple/`

## Runs tests/scripts

`poetry run pytest`

`poetry run black`

`poetry run python test_proj/test_proj.py`

If we want to run some part of a module directly, we have to modify the `pyproject.toml`

```
[tool.poetry.scripts]
test-script = "test_proj.test_proj:main"
```

`poetry run test_proj` (`poetry install` can be needed before in some cases)

## Venvs

`poetry shell`

or the old sourcing way

## Poetry.lock should be committed !

## For a lib :

`poetry build`

`poetry publish` (add `-r repository` for private ones)

(if the repo needs credential : `poetry config http-basic.foo username password` or other methods https://python-poetry.org/docs/repositories/)



