from django.core.management import BaseCommand

from ...models import Category


class Command(BaseCommand):
    """
    Create Category
    """

    def handle(self, *args, **options):
        self.stdout.write("Start create category")

        categories = [
            'Technology',
            'Health',
            'Travel',
            'Art',
            'Sport'
        ]

        for name in categories:
            category, is_created = Category.objects.get_or_create(name=name)
            if is_created:
                self.stdout.write(f"Category {name} is created")
            else:
                self.stdout.write(f"Category {name} already exits")

        self.stdout.write(self.style.SUCCESS("Categories are created"))
