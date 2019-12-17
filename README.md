# functional-ansible
Functional language experiments for ansible

## Current experiments

This current version contains a prototype implementation of the following functions:

* call_task: call a task by name and expand in memory

For this to be easily implemented we will want to execute this on the controller and do the expansion before anything else.

There are a few places where this could happenn, we do it just after the data is loaded from yaml but before it is compiled.

We implemented a new DataLoader module that runs the expansion after loading. For that we added a new configuration into ansible to allow for overloading the dataloader class and module by user configuration. We replace all the direct construction of that dataloader class with a factory method.

The template tasks are tested here,
`test/units/functional_modules/functional/call_task/test_call_task_simple.yml`
there is a new section added called template_tasks, this section is used for call_task. The variables all need to be defined in the file itself for this version.

## We want to implement these functions:

* yq: run jq/yq on lists of data
* cons : construct new variables in an elegant manner, to be called after the variables are all loaded.
* generate deb, rpm, setup, wheel distribution for a playbook
* refactor an existing playbook or role into one following best practices

