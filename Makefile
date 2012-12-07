check:
	python setup.py check

clean:
	find . -name *.pyc -delete

lint:
	which pyflakes >/dev/null || pip install --use-mirrors pyflakes
	arc lint

license:
	tail -13 LICENSE > LICENSE.short
	git ls-files | grep \.py$$ | xargs -n 1 bash bin/license.sh LICENSE.short
	rm LICENSE.short

check-index:
	if [[ $$(git status --porcelain | wc -l) -ne 0 ]]; then exit 1; fi

tag: check-index
	git tag $$(python setup.py --version)
	git push --tags

publish: check-index tag
	make license
	python setup.py sdist upload
	git reset --hard HEAD

test: clean
	python setup.py nosetests

test-matrix: clean
	which tox >/dev/null || pip install --use-mirrors tox
	tox

.PHONY: check clean test test-matrix license check-index tag publish lint
