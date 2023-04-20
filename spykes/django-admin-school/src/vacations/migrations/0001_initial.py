# Generated by Django 4.2 on 2023-04-20 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('init_date', models.DateField(verbose_name='init date')),
                ('end_date', models.DateField(verbose_name='end date')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employee', verbose_name='employee')),
            ],
            options={
                'verbose_name': 'Vacation',
                'verbose_name_plural': 'Vacations',
                'ordering': ['init_date'],
            },
        ),
    ]