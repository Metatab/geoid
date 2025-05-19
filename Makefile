.PHONY: default install reset check test tox readme docs publish clean

THIS_REV=$(shell python setup.py --version)
NEXT_REV=$(shell python -c "import sys; import semantic_version; \
print( semantic_version.Version('.'.join(sys.argv[1].split('.')[:3])).next_patch()  )\
" $(THIS_REV) )

MAKE := $(MAKE) --no-print-directory
	
test:
	python setup.py test
	
develop: 
	python setup.py develop 

# Display the version number
showrev:
	python -m setuptools_scm
	@echo this=$(THIS_REV) next=$(NEXT_REV)

# Create a new revision
rev:
	@echo this=$(THIS_REV) next=$(NEXT_REV)
	git tag $(NEXT_REV)
	python -m setuptools_scm


publish: 
	$(MAKE) clean
	git push --tags origin
	uv build
	$(MAKE) clean


check:
	$(MAKE) clean
	python setup.py sdist
	twine check dist/*
	$(MAKE) clean

clean:
	@rm -Rf *.egg .cache .coverage .tox build dist docs/build htmlcov
	@find . -depth -type d -name __pycache__ -exec rm -Rf {} \;
	@find . -type f -name '*.pyc' -delete