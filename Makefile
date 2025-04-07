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

upload: build
	twine upload dist/*
