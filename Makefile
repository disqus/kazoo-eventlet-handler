clean:
	find . -name *.pyc -delete

test: clean
	python setup.py nosetests

test-matrix: clean
	pip install --use-mirrors tox
	tox

.PHONY: clean test test-matrix
