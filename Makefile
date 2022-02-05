# Disable echoing of commands
MAKEFLAGS += --silent

# Ensure that Bash is used as the default shell
SHELL := /usr/bin/env bash

# The Python binary to use. Expects at least Python 3.8 available as python3. Use the
# PYTHON environment variable to change it. Do not change it here
PYTHON ?= python3
python := $(PYTHON)

# The modules to analyze
modules := auth

# Paths to all source files
source := $(shell find $(modules) -name '*.py' -not -name '__init__.py' 2>/dev/null)

# Paths to unit test targets
tests_path := tests
tests := $(shell find $(tests_path) -name '*.py' -not -name '__init__.py' 2>/dev/null)

.PHONY: documentation

# Perform all static analysis steps
static-analysis: dependency-check check-security-bugs type-check

# Check all dependencies for known security issues
dependency-check:
	source venv/bin/activate && safety check --full-report --file requirements.txt

# Check for security-related bugs
check-security-bugs:
	source venv/bin/activate && bandit -r $(modules)

# Ensure type-safety by checking for typing attributes
type-check:
	source venv/bin/activate && pyright $(source)

# Run all unit tests or do nothing if none are available
# Produces .coverage file for code coverage reporting
test:
ifneq ($(tests),)
	source venv/bin/activate && coverage run -m pytest $(tests)
endif

# Install necessary components
setup: install-virtual-environment install-dependencies

# Install the virtual environment
install-virtual-environment:
	$(python) -m venv venv

# Install all dependencies listed in requirements.txt
install-dependencies:
	source venv/bin/activate && $(python) -m pip install -r requirements.txt

# Generate all documents
documentation:
	source venv/bin/activate && PYTHONPATH=$(shell pwd) pdoc --force --html --config hljs_style=\'atom-one-light\' --output-dir documentation $(modules)

# Clean all dynamically created files
clean:
	rm -rf venv .pytest_cache .coverage documentation .hypothesis > /dev/null 2>&1 || exit 0
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
