# taken from ansible
.PHONY: tests-py3
ANSIBLE_TEST ?= bin/ansible-test
TEST_FLAGS ?=
#PYTHON3_VERSION ?= $(shell python3 -c 'import sys; print("%s.%s" % sys.version_info[:2])')
PYTHON3_VERSION=3.7

test_playbook:
	PYTHONPATH=lib/ ANSIBLE_DATA_LOADER_MODULE_NAME=functional_ansible.parsing.dataloader ANSIBLE_STRATEGY_PLUGINS=lib/functional_ansible/plugins/strategy/ python3  ~/.local/bin/ansible-playbook --connection=local ~/functional-ansible/test/units/functional_modules/functional/call_task/test_call_task_simple.yml -vvvvvv

tests-py3:
	# ANSIBLE_TEST_CONTENT_ROOT=test/functional_units/
	ANSIBLE_DATA_LOADER_MODULE_NAME=functional_ansible.parsing.dataloader PYTHONPATH=./lib:./src/ansible/test/lib/:./src/ansible/test/ $(ANSIBLE_TEST) units -vvvv --python $(PYTHON3_VERSION) $(TEST_FLAGS)  --verbose --debug --pdb
# test/functional_units/
