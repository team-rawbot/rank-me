#!/usr/bin/env python
import glob
import os
import sys

if __name__ == "__main__":
    if 'test' in sys.argv:
        env_dir = os.path.join('tests', 'envdir')
    else:
        env_dir = 'envdir'
    env_vars = glob.glob(os.path.join(env_dir, '*'))
    for env_var in env_vars:
        with open(env_var, 'r') as env_var_file:
            os.environ.setdefault(env_var.split(os.sep)[-1],
                                  env_var_file.read().strip())

    # If no DJAJGO_SETTINGS_MODULE is set, use the local one
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rankme.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
