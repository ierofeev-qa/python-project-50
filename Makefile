install:
	poetry install

show-diff:
	poetry run gendiff $(format) $(first_file) $(second_file)

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl --force-reinstall

lint:
	poetry run flake8 gendiff

run-tests:
	poetry run coverage run -m pytest
	poetry run coverage xml