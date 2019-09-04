'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from __future__ import with_statement

from mu_repo.print_ import Print
import os.path
from mu_repo import Status
from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel


#===================================================================================================
# Run
#===================================================================================================
def Run(params, on_output=None):
    args = params.args
    config = params.config

    base_path = None
    command_name = args[1]
    path_index = get_path_index(args)

    if command_name == 'add':
        if path_index < 0:
            msg = 'Define a path to create worktree.'
            Print(msg)
            return Status(msg, True, config)

        base_path = os.path.abspath(args[path_index])
        if not os.path.exists(base_path):
            msg = 'Path %s does not exist' % (args[path_index], )
            Print(msg)
            return Status(msg, True, config)

    if not config.repos:
        msg = 'No repository registered. Use mu register repo_name to register repository.'
        Print(msg)
        return Status(msg, True, config)

    commands = []
    for repo in config.repos:
        if not os.path.exists(repo):
            Print('%s does not exist' % (repo,))
        else:
            if command_name == 'add':
                repo_name = os.path.basename(os.path.abspath(repo))
                args[path_index] = os.path.join(base_path, repo_name)

            commands.append(ParallelCmd(repo, [config.git] + args))

    ExecuteInParallel(commands, on_output, serial=config.serial)

    return Status('Finished', True)


def get_path_index(args):
    prev_arg = ''
    for idx, arg in enumerate(args):
        if arg in ['worktree', 'add']:
            prev_arg = arg
            continue
        if arg.startswith('-'):
            prev_arg = arg
            continue
        if prev_arg in ['-b', '-B', '--expire', '--reason']:
            prev_arg = arg
            continue
        return idx
    return -1
