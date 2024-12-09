from django.core.management import BaseCommand

from ...models import Tag


class Command(BaseCommand):
    """
    Create Tags
    """

    def handle(self, *args, **options):
        self.stdout.write("Start create tags")

        tags = [
            'math',
            'science',
            'game',
            'coffee',
            'quadrants'
        ]

        for name in tags:
            tag, is_created = Tag.objects.get_or_create(name=name)
            if is_created:
                self.stdout.write(f"Tag {name} is created")
            else:
                self.stdout.write(f"Tag {name} already exits")

        self.stdout.write(self.style.SUCCESS("Tags are created"))
