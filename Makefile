clean:
	find . -name *.pyc -delete

test: clean
	python setup.py nosetests

test-matrix: clean
	which tox >/dev/null || pip install --use-mirrors tox
	tox

.PHONY: clean test test-matrix
