# Generated by Django 3.2.3 on 2022-03-18 01:26

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
                ('gender', models.CharField(blank=True, choices=[('female', 'female'), ('male', 'male'), ('other', 'other')], max_length=6, null=True, verbose_name='جنسیت')),
                ('avatar', models.ImageField(blank=True, help_text='JPG, JPEG or PNG is validate', null=True, upload_to=main_app.models.user_image_profile_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), main_app.models.validate_image_size], verbose_name='عکس پروفایل')),
                ('bio', models.CharField(blank=True, max_length=1000, null=True, verbose_name='بیو')),
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='شهر')),
            ],
            options={
                'verbose_name': 'شهر',
                'verbose_name_plural': 'شهر ها',
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
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')),
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
            name='Hangout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='نام')),
                ('datetime', models.DateTimeField(verbose_name='زمان برگذاری')),
                ('description', models.CharField(max_length=100, verbose_name='توضیحات')),
                ('address', models.CharField(max_length=300, verbose_name='آدرس')),
                ('gender', models.CharField(choices=[('female', 'female'), ('male', 'male'), ('other', 'other')], max_length=10, verbose_name='جنسیت')),
                ('province', models.CharField(choices=[('ea', 'آذربایجان شرقی'), ('wa', 'آذربایجان غربی'), ('ard', 'اردبیل'), ('esf', 'اصفهان'), ('alb', 'البرز'), ('ila', 'ایلام'), ('bus', 'بوشهر'), ('teh', 'تهران'), ('cha', 'چهارمحال و بختیاری'), ('khs', 'خراسان جنوبی'), ('khn', 'خراسان شمالی'), ('khr', 'خراسان رضوی'), ('khu', 'خوزستان'), ('zan', 'زنجان'), ('sem', 'سمنان'), ('sis', 'سیستان و بلوچستان'), ('far', 'فارس'), ('qaz', 'قزوین'), ('qom', 'قم'), ('kor', 'کردستان'), ('ker', 'کرمان'), ('kermanshah', 'کرمانشاه'), ('koh', 'کهگیلویه و بویر احمد'), ('gol', 'گلستان'), ('gil', 'گیلان'), ('lor', 'لرستان'), ('maz', 'مازندران'), ('mar', 'مرکزی'), ('hor', 'هرمزگان'), ('ham', 'همدان'), ('yazd', 'یزد')], max_length=20, verbose_name='استان')),
                ('status', models.CharField(choices=[('pr', 'خصوصی'), ('pu', 'عمومی')], max_length=2, verbose_name='وضعیت')),
                ('min_age', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(12), django.core.validators.MaxValueValidator(50)], verbose_name='حداقل سن')),
                ('max_age', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(16), django.core.validators.MaxValueValidator(70)], verbose_name='حداکثر سن')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='هزینه')),
                ('type', models.CharField(blank=True, choices=[('e', 'علمی'), ('v', 'ورزشی'), ('a', 'هنری')], max_length=30, null=True, verbose_name='نوع پاتوق')),
                ('place', models.CharField(blank=True, choices=[('p', 'پارک'), ('m', 'موزه'), ('c', 'کافه'), ('r', 'رستوران '), ('c', 'سینما')], max_length=40, null=True, verbose_name='مکان')),
                ('is_over', models.BooleanField(default=False, verbose_name='تمام شده')),
                ('duration', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='مدت برگزاری')),
                ('repeat', models.CharField(blank=True, choices=[('n', 'هیچکدام'), ('w', 'هر هفته'), ('m', 'هر ماه')], default='n', max_length=1, null=True, verbose_name='تکرار')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hangout_creator', to=settings.AUTH_USER_MODEL, verbose_name='سازنده')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='اعضا')),
            ],
            options={
                'verbose_name': 'پاتوق',
                'verbose_name_plural': 'پاتوق ها',
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
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='نام')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='توضیحات')),
                ('date', models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('photo', models.ImageField(blank=True, help_text='JPG, JPEG or PNG is validate', null=True, upload_to=main_app.models.party_image_profile_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), main_app.models.validate_image_size], verbose_name='عکس اکیپ')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL, verbose_name='سازنده')),
                ('members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='اعضا')),
            ],
            options={
                'verbose_name': 'اکیپ',
                'verbose_name_plural': 'اکیپ ها',
                'ordering': ['-date'],
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
