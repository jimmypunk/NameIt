from django.core.management.base import BaseCommand
from smart_naming.models import RepoWordCountView


class Command(BaseCommand):
    help = 'build tries from record in database'

    def add_arguments(self, parser):
        # parser.add_argument('kerker', nargs='+', type=str)
        pass

    def handle(self, *args, **options):