# Generated by Django 2.1.5 on 2020-07-30 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Save',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('post_id', models.CharField(max_length=150)),
                ('img_url', models.CharField(max_length=150)),
                ('category', models.CharField(max_length=10)),
                ('author', models.CharField(max_length=150)),
                ('post_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]