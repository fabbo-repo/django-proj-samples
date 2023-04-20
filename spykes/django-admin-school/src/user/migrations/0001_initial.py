# Generated by Django 4.2 on 2023-04-20 09:37

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(help_text='Maximum 150 characters and minimum 1 character.', max_length=150, validators=[django.core.validators.MinLengthValidator(1)], verbose_name='first name')),
                ('last_name', models.CharField(help_text='Maximum 150 characters and minimum 1 character.', max_length=150, validators=[django.core.validators.MinLengthValidator(1)], verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('dni', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='dni')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('nationality', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='nationality')),
            ],
            options={
                'verbose_name': 'Nationality',
                'verbose_name_plural': 'Nationalities',
                'ordering': ['nationality'],
            },
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('appuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('user.appuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('appuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('vacation_days', models.IntegerField(blank=True, default=0, help_text='Number of available vacation days', verbose_name='vacation days')),
                ('bank_account', models.CharField(blank=True, help_text='IBAN should have between 15 and 34 characters.', max_length=200, null=True, validators=[django.core.validators.MinLengthValidator(15), django.core.validators.MaxLengthValidator(34)], verbose_name='bank account')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'ordering': ['-date_joined'],
                'abstract': False,
            },
            bases=('user.appuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('appuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('passport', models.CharField(blank=True, max_length=500, null=True, unique=True, verbose_name='passport')),
                ('course_code', models.CharField(blank=True, help_text='Enrolled course code', max_length=50, null=True, verbose_name='course code')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'ordering': ['-date_joined'],
                'abstract': False,
            },
            bases=('user.appuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='appuser',
            name='nationality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.nationality', verbose_name='nationality'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]