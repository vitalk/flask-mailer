help:
	@echo "Please use \`make <target>\` where target one of"
	@echo " test		to run the test suite"
	@echo " coverage	to report tests coverage"
	@echo " clean		to clean package directory"


test:
	python setup.py test


coverage:
	python setup.py test --coverage


clean:
	@rm -rf build dist *.egg-info
	@find . -name '*.py[co]' -exec rm -f {} +
