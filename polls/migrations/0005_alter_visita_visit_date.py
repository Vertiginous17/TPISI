# Generated by Django 4.1.dev20211115193433 on 2021-11-22 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_alter_visita_visit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visita',
            name='visit_date',
            field=models.DateField(),
        ),
    ]
