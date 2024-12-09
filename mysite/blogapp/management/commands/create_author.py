from django.core.management import BaseCommand

from ...models import Author


class Command(BaseCommand):
    """
    Create Authors
    """

    def handle(self, *args, **options):
        self.stdout.write("Start create authors")

        authors_info = [
            ('Ben', 'no bio'),
            ('Maxim', 'no bio'),
            ('Danila', 'no bio'),
            ('Andrey', 'no bio'),
        ]

        for name, bio in authors_info:
            guy, is_created = Author.objects.get_or_create(name=name, bio=bio)
            if is_created:
                self.stdout.write(f"Author {name} is created")
            else:
                self.stdout.write(f"Author {name} already exits")

        self.stdout.write(self.style.SUCCESS("Authors are created"))
