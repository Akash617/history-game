# Generated by Django 4.2.5 on 2023-09-15 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_event_category_event_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='topic',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
