import os
import sys

from django.db import connection

from django.core.management.base import BaseCommand, CommandError
from django_mask.parser import parse_config
from django_mask.utils import progress


class Command(BaseCommand):
    help = "Masks model fields (database columns) for hiding sensitive information"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-p", "--path",
            dest="conf_path",
            help="Path to yaml config file with masking tasks"
        )
        parser.add_argument(
            "-c", "--chunks",
            dest="chunks",
            type=int,
            default=500,
            help="Number of rows that will update in single sql query"
        )

    def handle(self, *args, **options):
        conf_path = options["conf_path"]
        if conf_path is None:
            raise CommandError("config file not provided")

        if not os.path.exists(conf_path):
            raise CommandError("file with path \"{}\" not exists".format(conf_path))

        file_content = ""
        with open(conf_path) as file:
            file_content = file.read()

        task, errors = parse_config(file_content)
        if errors:
            for error in errors:
                error.display()
                sys.stderr.write("\n")
            return

        self.stdout.write("Config parsed...\n")
        self.stdout.write("Updating database...\n")

        update_tasks = task.get_update_tasks(options["chunks"])
        total_count = len(update_tasks)
        cursor = connection.cursor()

        for counter, update_task in enumerate(update_tasks, 1):
            update_task.process(cursor=cursor)
            progress(counter, total_count)

        self.stdout.write("\n")
        self.stdout.write("Done")
