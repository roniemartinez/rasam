install:
	pip3 install -U pip poetry==1.0.5
	poetry install

style:
	poetry run autoflake --remove-all-unused-imports --in-place -r --exclude __init__.py .
	poetry run isort -rc --atomic .
	poetry run black .
	poetry run flake8 .

type:
	poetry run mypy --ignore-missing-imports rasam rasam/components tests/components

test:
	poetry run pytest --cov=rasam --cov-report=xml  --cov-report=html -vv
