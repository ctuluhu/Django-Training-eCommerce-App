# Generated by Django 2.1 on 2018-08-20 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='email_address',
            new_name='emailAddress',
        ),
    ]