# Generated by Django 3.2.4 on 2021-07-24 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AgahSurvey', '0015_auto_20210723_1109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['answersheet', 'question'], 'verbose_name': 'پاسخ', 'verbose_name_plural': 'پاسخ'},
        ),
    ]