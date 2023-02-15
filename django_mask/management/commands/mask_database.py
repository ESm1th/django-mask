from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Masks model fields (database columns) for hiding sensitive information"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to config file in \"yaml\" format"
        )

    def handle(self, *args, **options):
        if "file_path" not in options:
            raise CommandError("Config file path not provided")
