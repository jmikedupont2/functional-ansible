
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
#from units.compat import unittest
from mock import patch, MagicMock

from ansible.executor.play_iterator import PlayIterator
from ansible.playbook import Playbook
from ansible.playbook.play_context import PlayContext
from ansible.plugins.strategy.linear import StrategyModule
from ansible.executor.task_queue_manager import TaskQueueManager

from units.mock.loader import DictDataLoader
from units.mock.path import mock_unfrackpath_noop

import pytest
import sys
import os

file_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.abspath(os.path.join(file_root, '..', '..','..', '..'))
lib_root = os.path.join(project_root, 'lib')
# source_root3 = os.path.join(ansible_root, 'test')
if os.path.exists(lib_root):
    sys.path.insert(0, lib_root)
else:
     raise Exception("Missing"+ lib_root)            
# if os.path.exists(source_root3):
#     sys.path.insert(0, source_root3)
# else:
#     raise Exception("Missing"+ source_root3)
# print(sys.path)

from units.module_utils import set_module_args
#import pdb
#pdb.set_trace()
# import sys
# print(sys.path)
# import functional_ansible.modules.functional.call_task as call_task

# def test_simple_call_task():
#     set_module_args({
#         "name": "call_task",
#         "task": 'simple_task',
#     })
#     #with pytest.raises(SystemExit):
#     print(call_task.main())

from functional_ansible.plugins.strategy.functional_loader import StrategyModule

class TestStrategyFunctional(unittest.TestCase):

    @patch('ansible.playbook.role.definition.unfrackpath', mock_unfrackpath_noop)
    def test_noop(self):
        fake_loader = DictDataLoader({
            "test_play.yml": """
            - hosts: localhost
              gather_facts: no
              tasks:
              - name: simple_function
                debug:
                  msg : 'hello world'
                tags:
                 - functional

              - name: call_simple_function
                call_task:
                  name : "simple_function"

            """,
        })

        mock_var_manager = MagicMock()
        mock_var_manager._fact_cache = dict()
        mock_var_manager.get_vars.return_value = dict()

        p = Playbook.load('test_play.yml', loader=fake_loader, variable_manager=mock_var_manager)

        inventory = MagicMock()
        inventory.hosts = {}
        hosts = []

        host = MagicMock()
        host.name = host.get_name.return_value = 'localhost'
        hosts.append(host)
        inventory.hosts[host.name] = host
        
        inventory.get_hosts.return_value = hosts
        inventory.filter_hosts.return_value = hosts

        mock_var_manager._fact_cache['localhost'] = dict()

        play_context = PlayContext(play=p._entries[0])

        itr = PlayIterator(
            inventory=inventory,
            play=p._entries[0],
            play_context=play_context,
            variable_manager=mock_var_manager,
            all_vars=dict(),
        )

        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=mock_var_manager,
            loader=fake_loader,
            passwords=None,
            forks=5,
        )
        tqm._initialize_processes(3)
        strategy = StrategyModule(tqm)
        strategy._hosts_cache = [h.name for h in hosts]
        strategy._hosts_cache_all = [h.name for h in hosts]

        # implicit meta: flush_handlers
        hosts_left = strategy.get_hosts_left(itr)
        hosts_tasks = strategy._get_next_task_lockstep(hosts_left, itr)
        host1_task = hosts_tasks[0][1]
        host2_task = hosts_tasks[1][1]

