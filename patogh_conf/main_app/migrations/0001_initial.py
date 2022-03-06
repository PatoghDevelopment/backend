# Generated by Django 3.2.3 on 2022-03-06 14:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main_app.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='نام کاربری')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام خانوادگی')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='ایمیل')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('gender', models.CharField(blank=True, choices=[('0', 'female'), ('1', 'male')], default='1', max_length=6, null=True, verbose_name='جنسیت')),
                ('avatar', models.ImageField(blank=True, help_text='JPG, JPEG or PNG is validate', null=True, upload_to=main_app.models.user_image_profile_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), main_app.models.validate_image_size], verbose_name='عکس پروفایل')),
                ('bio', models.CharField(blank=True, max_length=1000, null=True, verbose_name='درباره')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this Tag', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('name', models.CharField(max_length=50, verbose_name='شهر')),
            ],
            options={
                'verbose_name': 'شهر',
                'verbose_name_plural': 'شهر ها',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this party', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='نام')),
                ('avatar', models.ImageField(blank=True, help_text='JPG, JPEG or PNG is validate', null=True, upload_to=main_app.models.party_image_profile_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), main_app.models.validate_image_size], verbose_name='عکس اکیپ')),
                ('description', models.CharField(help_text='descripe your party', max_length=1000, verbose_name='توضیحات')),
                ('creation_time', models.DateTimeField(auto_now_add=True, help_text='Creation time for the party', verbose_name='زمان ساخت اکیپ')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='پدید آورنده')),
            ],
            options={
                'verbose_name': 'اکیپ',
                'verbose_name_plural': 'اکیپ ها',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Patogh',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this gathering', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام')),
                ('profile_image', models.ImageField(blank=True, help_text='JPG, JPEG or PNG is validate', null=True, upload_to=main_app.models.patogh_image_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), main_app.models.validate_image_size], verbose_name='عکس پاتوق')),
                ('description', models.CharField(help_text='descripe your patogh', max_length=1000, verbose_name='توضیحات')),
                ('type', models.CharField(choices=[('0', 'public'), ('1', 'private')], default='0', max_length=10, verbose_name='حالت دورهمی')),
                ('creation_time', models.DateTimeField(auto_now_add=True, help_text='Creation time for the patogh', null=True, verbose_name='زمان ساخت پاتوق')),
                ('start_time', models.DateTimeField(help_text='Start time for the patogh', null=True, verbose_name='زمان شروع')),
                ('end_time', models.DateTimeField(help_text='end time for the patogh', null=True, verbose_name='زمان پایان')),
                ('address', models.CharField(blank=True, max_length=1000, null=True, verbose_name='آدرس')),
            ],
            options={
                'verbose_name': 'پاتوق',
                'verbose_name_plural': 'پاتوق ها',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PatoghCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this Category', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('name', models.CharField(max_length=50, verbose_name='کتگوری')),
            ],
            options={
                'verbose_name': 'کتگوری',
                'verbose_name_plural': 'کتگوری ها',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PendingVerify',
            fields=[
                ('receptor', models.EmailField(default='a@a.com', max_length=50, primary_key=True, serialize=False, verbose_name='دریافت کننده')),
                ('otp', models.IntegerField(verbose_name='OTP کد')),
                ('send_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان ارسال')),
                ('allowed_try', models.SmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name=' دفعات مجاز برای تلاش')),
            ],
            options={
                'verbose_name': 'تاییدیه',
                'verbose_name_plural': 'تاییدیه ها',
                'ordering': ['send_time'],
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('description', models.TextField(max_length=2000, verbose_name='متن پیام')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ')),
            ],
            options={
                'verbose_name': 'پشتیبانی',
                'verbose_name_plural': 'پشتیبانی ها',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this Tag', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('tag', models.CharField(max_length=40, unique=True, verbose_name='برچسب')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب ها',
                'ordering': ['id'],
                'unique_together': {('id', 'tag')},
            },
        ),
        migrations.CreateModel(
            name='PatoghMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('0', 'admin'), ('1', 'normal participant')], default='1', help_text='سطح دسترسی کاربر را مشخص کنید', max_length=10, verbose_name='مجوز کاربر')),
                ('time', models.DateTimeField(auto_now_add=True, help_text='attend patogh time', verbose_name='زمان پیوستن')),
                ('email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='شناسه کاربر')),
                ('patogh_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.patogh', verbose_name='شناسه پاتوق')),
            ],
            options={
                'verbose_name': 'عضو پاتوق',
                'verbose_name_plural': 'اعضای پاتوق',
                'ordering': ['patogh_id'],
            },
        ),
        migrations.AddField(
            model_name='patogh',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.patoghcategory', verbose_name='نوع پاتوق'),
        ),
        migrations.AddField(
            model_name='patogh',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.city', verbose_name='شهر'),
        ),
        migrations.AddField(
            model_name='patogh',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='شناسه پدید آورنده'),
        ),
        migrations.CreateModel(
            name='PartyMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[('0', 'no'), ('1', 'yes')], default='0', verbose_name='سطح دسترسی کاربر به اکیپ')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('party_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.party', verbose_name='اکیپ')),
            ],
            options={
                'verbose_name': 'عضو اکیپ',
                'verbose_name_plural': 'اعضای اکیپ',
                'ordering': ['party_id'],
            },
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('a', 'پاسخ داده شده'), ('w', 'در انتظار')], max_length=1, null=True, verbose_name='وضعیت')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='گیرنده')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='فرستنده')),
            ],
            options={
                'verbose_name': 'درخواست دوستی',
                'verbose_name_plural': 'درخواست های دوستی',
                'ordering': ['-datetime'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.city', verbose_name='شهر'),
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='دوستان'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='parties',
            field=models.ManyToManyField(blank=True, through='main_app.PartyMembers', to='main_app.Party'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='UsersHaveFriends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.SmallIntegerField(choices=[(0, 'rejected'), (1, 'pending answer'), (2, 'accepted')], default=1, verbose_name='وضعیت دوستی')),
                ('time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان درخواست دوستی')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reciver_set', to=settings.AUTH_USER_MODEL, verbose_name='گیرنده')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender_set', to=settings.AUTH_USER_MODEL, verbose_name='فرستنده')),
            ],
            options={
                'verbose_name': 'وضعیت درخواست',
                'verbose_name_plural': 'وضعیت درخواست ها',
                'ordering': ['time'],
                'unique_together': {('sender', 'receiver')},
            },
        ),
    ]
