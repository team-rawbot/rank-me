#!/usr/bin/env python
import os
import sys

from rankme.utils import get_project_root_path, import_env_vars

if __name__ == "__main__":
    import_env_vars(os.path.join(get_project_root_path(), 'envdir'))

    # If no DJANGO_SETTINGS_MODULE is set, use the local one
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rankme.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
