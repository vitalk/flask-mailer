help:
	@echo "Please use \`make <target>\` where target one of"
	@echo " test		to run the test suite"
	@echo " coverage	to report tests coverage"


test:
	python setup.py test


coverage:
	python setup.py test --coverage
