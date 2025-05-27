clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ __pycache__/ .mypy_cache/ .coverage htmlcov .tox .venv venv/
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +


build: clean
	python -m build

format:
	black .
	flake8

test:
	pip install ".[all]"
	black --check .
	flake8
	pytest tests

docs-serve:
	pip install ".[all]"
	mkdocs serve --clean

docs-deploy:
	pip install ".[all]"
	mkdocs gh-deploy --clean

upload: build
	twine check --strict dist/*
	twine upload dist/*
