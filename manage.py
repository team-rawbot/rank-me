#!/usr/bin/env python
import os
import sys

from rankme import get_project_root_path, import_env_vars

if __name__ == "__main__":
    if 'test' in sys.argv:
        env_dir = os.path.join('tests', 'envdir')
    else:
        env_dir = 'envdir'

    import_env_vars(os.path.join(get_project_root_path(), env_dir))

    # If no DJANGO_SETTINGS_MODULE is set, use the local one
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rankme.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
