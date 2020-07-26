# Generated by Django 3.0.8 on 2020-07-22 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userpage', '0004_auto_20200722_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='userpage.Post')),
                ('user', models.ManyToManyField(related_name='likinguser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
