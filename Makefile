clean:
	rm -rf dist/ build/ *.egg-info

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
