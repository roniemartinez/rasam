install:
	pip3 install poetry==1.0.5
	poetry install

style:
	poetry run autoflake --remove-all-unused-imports --in-place -r --exclude __init__.py .
	poetry run isort -rc --atomic .
	poetry run black --exclude setup.py .
	poetry run flake8 .

type:
	poetry run mypy --ignore-missing-imports rasam rasam/components rasam/importers tests/components tests/importers

test:
	poetry run pytest --cov=rasam --cov-report=xml --cov-report=html -vv

setup:
	poetry run dephell deps convert
