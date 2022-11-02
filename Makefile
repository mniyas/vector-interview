# Arcane incantation to print all the other targets, from https://stackoverflow.com/a/26339924
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# Install exact Python version
conda-update:
	conda env update --prune -f environment.yml

# Compile and install exact pip packages
pip-tools:
	pip install pip-tools
	pip-compile requirements/dev-lint.in -o requirements/dev-lint.txt -r
	pip-compile requirements/dev.in -o requirements/dev.txt -r
	pip-compile requirements/prod.in -o requirements/prod.txt -r
	pip-sync requirements/dev-lint.txt requirements/dev.txt requirements/prod.txt