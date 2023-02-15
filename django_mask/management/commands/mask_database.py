import sys

from django.core.management.base import BaseCommand, CommandError
from django_mask.parser import parse_config


class Command(BaseCommand):
    help = "Masks model fields (database columns) for hiding sensitive information"

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError("Config file path not provided")

        config_file_path = args[1]
        file_content = ""

        with open(config_file_path) as file:
            file_content = file.read()

        task, errors = parse_config(file_content)
        if errors:
            for error in errors:
                error.display()
            return
        sys.stdout.write = "Config parsed"
