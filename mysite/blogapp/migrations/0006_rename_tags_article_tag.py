# Generated by Django 5.1.1 on 2024-11-10 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_article_title_author_name_category_name_tag_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='tags',
            new_name='tag',
        ),
    ]