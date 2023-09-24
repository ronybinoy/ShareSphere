# Generated by Django 4.2.4 on 2023-09-22 10:30

from django.conf import settings
import django.contrib.auth.models
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
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('img', models.ImageField(default='https://img.freepik.com/free-icon/man_318-677829.jpg', null=True, upload_to='pics')),
                ('is_migrant', models.BooleanField(default=False, null=True, verbose_name='is_migrant')),
                ('is_institute', models.BooleanField(default=False, null=True, verbose_name='is_institute')),
                ('is_landlord', models.BooleanField(default=False, null=True, verbose_name='is_landlord')),
                ('migrant_uid', models.CharField(default='', max_length=20, null=True, verbose_name='migrant_uid')),
                ('institute_lis_no', models.CharField(default='', max_length=30, null=True, verbose_name='institute_lis_no')),
                ('landlord_uid', models.CharField(default='', max_length=20, null=True, verbose_name='landlord_uid')),
                ('nationality', models.CharField(default='', max_length=30, null=True, verbose_name='nationality')),
                ('region', models.CharField(default='', max_length=30, null=True, verbose_name='region')),
                ('institute_type', models.CharField(default='', max_length=20, null=True, verbose_name='institute_type')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
            name='Inst_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=12, unique=True)),
                ('inst_name', models.CharField(max_length=255)),
                ('inst_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='main.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255)),
                ('course_mode', models.CharField(default='Online', max_length=255)),
                ('course_type', models.CharField(default='Bachelor Degree', max_length=255)),
                ('academic_disciplines', models.CharField(default='Business and Information Technology', max_length=255)),
                ('course_desc', models.TextField(null=True)),
                ('eligibility', models.TextField()),
                ('duration', models.CharField(max_length=255)),
                ('fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('opendate', models.DateField()),
                ('appdeadline', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('thumbnail_image', models.ImageField(blank=True, null=True, upload_to='course_thumbnails/')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='', max_length=254)),
                ('gender', models.CharField(default='', max_length=10)),
                ('date_of_birth', models.DateField(default='')),
                ('citizenship', models.CharField(default='', max_length=255)),
                ('country', models.CharField(default='', max_length=100)),
                ('province', models.CharField(default='', max_length=100)),
                ('street_address1', models.CharField(default='', max_length=255)),
                ('street_address2', models.CharField(blank=True, default='', max_length=255)),
                ('postal_code', models.CharField(default='', max_length=20)),
                ('contact_number', models.CharField(default='', max_length=20)),
                ('qualification1', models.CharField(default='', max_length=255)),
                ('institute1', models.CharField(default='', max_length=255)),
                ('percentage1', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('passing_year1', models.IntegerField(default=0)),
                ('english_proficiency_test', models.CharField(default='', max_length=10)),
                ('english_score', models.DecimalField(decimal_places=2, default='', max_digits=4)),
                ('english_validity', models.IntegerField(default=0)),
                ('proficiency_result', models.FileField(null=True, upload_to='proficiency_results/')),
                ('policy_declaration', models.BooleanField(default=True)),
                ('average_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
