from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints \"Hello World\" to the screen"

    def add_arguments(self, parser):
        parser.add_argument("text", type=str)

    def handle(self, *args, **options):
        self.stdout.write("Hello World - {}".format(options["text"]))
