import os
import sys

from django.core.management import call_command
from django.test import TestCase


class MigrationTestCase(TestCase):
    def test_missing_migrations(self):
        """
        Test and assert that all models are fully covered by migrations.
        Any missing migrations will fail this test.
        """
        sys.stdout = open(os.devnull, "w")  # Stop print statement
        call_command("makemigrations", "--check", "--no-input", "--dry-run")
        sys.stdout = sys.__stdout__  # Enable print statement
