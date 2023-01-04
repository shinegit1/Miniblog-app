import os

import pytest
from django.core.management import call_command

from miniblog.settings import BASE_DIR

file_path = os.path.join(BASE_DIR, 'relative_path')


@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        test_db_file_path = os.path.join(BASE_DIR, 'blog/tests/test_data/test_db.json')
        call_command('loaddata', test_db_file_path)
