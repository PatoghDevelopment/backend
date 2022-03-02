# Generated by Django 3.2.3 on 2022-03-02 11:57

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
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='نام کاربری')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام خانوادگی')),
                ('email', models.EmailField(max_length=50, primary_key=True, serialize=False, verbose_name='ایمیل')),
                ('mobile_number', models.CharField(blank=True, max_length=12, null=True, unique=True, verbose_name='شماره تلفن')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('gender', models.CharField(blank=True, choices=[('0', 'female'), ('1', 'male')], default='1', max_length=6, null=True, verbose_name='جنسیت')),
                ('avatar', models.ImageField(blank=True, help_text='JPG, JPEG or PNG is validate', null=True, upload_to=main_app.models.user_image_profile_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), main_app.models.validate_image_size], verbose_name='عکس پروفایل')),
                ('bio', models.CharField(blank=True, max_length=1000, null=True, verbose_name='درباره')),
                ('score', models.IntegerField(blank=True, default=0, null=True, verbose_name='امتیاز کاربر')),
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
            name='LocationTypes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this location type', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('name', models.CharField(max_length=30, verbose_name='نوع مکان')),
            ],
            options={
                'verbose_name': 'مکان',
                'verbose_name_plural': 'مکان ها',
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
                ('start_time', models.DateTimeField(help_text='Start time for the patogh', null=True, verbose_name='زمان شروع')),
                ('end_time', models.DateTimeField(help_text='end time for the patogh', null=True, verbose_name='زمان پایان')),
            ],
            options={
                'verbose_name': 'دورهمی',
                'verbose_name_plural': 'دورهمی ها',
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
            name='PatoghInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this gathering', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام')),
                ('profile_image', models.ImageField(blank=True, help_text='JPG, JPEG or PNG is validate', null=True, upload_to=main_app.models.patogh_image_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), main_app.models.validate_image_size], verbose_name='عکس پاتوق')),
                ('description', models.CharField(help_text='descripe your patogh', max_length=1000, verbose_name='توضیحات')),
                ('type', models.CharField(choices=[('0', 'public'), ('1', 'private')], default='1', max_length=10, verbose_name='حالت دورهمی')),
                ('creation_time', models.DateTimeField(auto_now_add=True, help_text='Creation time for the patogh', verbose_name='زمان ساخت پاتوق')),
                ('address', models.CharField(blank=True, max_length=1000, null=True, verbose_name='آدرس')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.patoghcategory', verbose_name='نوع پاتوق')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.city', verbose_name='شهر')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='شناسه پدید آورنده')),
            ],
            options={
                'verbose_name': 'دورهمی',
                'verbose_name_plural': 'دورهمی ها',
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
            name='Tags',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this Tag', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('tag', models.CharField(max_length=40, unique=True, verbose_name='برچسب')),
            ],
            options={
                'verbose_name': 'برچست',
                'verbose_name_plural': 'برچسب ها',
                'ordering': ['id'],
                'unique_together': {('id', 'tag')},
            },
        ),
        migrations.CreateModel(
            name='PatoghsComments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique Id for this patogh Commments', primary_key=True, serialize=False, verbose_name='شناسه')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')),
                ('comment', models.CharField(max_length=1000, verbose_name='نظر')),
                ('patogh_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.patogh', verbose_name='شناسه پاتوق')),
                ('reply_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.patoghscomments', verbose_name='بازخورد به')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='فرستنده')),
            ],
            options={
                'verbose_name': 'نظر در مورد پاتوق',
                'verbose_name_plural': 'نظرات در مورد پاتوق',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PatoghMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('0', 'admin'), ('1', 'normal participant')], default='1', help_text='سطح دسترسی کاربر را مشخص کنید', max_length=10, verbose_name='مجوز کاربر')),
                ('time', models.DateTimeField(auto_now_add=True, help_text='attend patogh time', verbose_name='زمان پیوستن')),
                ('email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='شناسه کاربر')),
                ('patogh_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.patoghinfo', verbose_name='شناسه پاتوق')),
            ],
            options={
                'verbose_name': 'عضو دورهمی',
                'verbose_name_plural': 'اعضای دورهمی',
                'ordering': ['patogh_id'],
            },
        ),
        migrations.CreateModel(
            name='PatoghHaveImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(blank=True, help_text='JPG, JPEG or PNG is validate', null=True, upload_to=main_app.models.dorhami_image_profile_directory_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), main_app.models.validate_image_size], verbose_name='عکس برای دورهمی')),
                ('status', models.SmallIntegerField(choices=[(0, 'registered'), (1, 'accepted'), (2, 'rejected'), (3, 'deleted')], default=0, verbose_name='وضعیت تایید عکس')),
                ('send_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان ارسال')),
                ('patogh_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.patogh', verbose_name='شناسه پاتوق')),
            ],
            options={
                'verbose_name': 'عکس پاتوق',
                'verbose_name_plural': 'عکس های پاتوق',
                'ordering': ['patogh_id'],
            },
        ),
        migrations.AddField(
            model_name='patogh',
            name='patogh_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.patoghinfo', verbose_name='شناسه اطلاعات پاتوق'),
        ),
        migrations.CreateModel(
            name='PartyMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[('0', 'no'), ('1', 'yes')], default='0', verbose_name='سطح دسترسی کاربر به اکیپ')),
                ('g_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.party', verbose_name='اکیپ')),
            ],
            options={
                'verbose_name': 'عضو اکیپ',
                'verbose_name_plural': 'اعضای اکیپ',
                'ordering': ['p_id'],
                'unique_together': {('p_id', 'g_id')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.city', verbose_name='شهر'),
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
        migrations.CreateModel(
            name='reportedPatogh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('massage', models.CharField(max_length=1000, verbose_name='پیام')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')),
                ('patogh_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.patogh', verbose_name='شناسه پاتوق')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='نام کاربری')),
            ],
            options={
                'verbose_name': 'پاتوق گزارش شده',
                'verbose_name_plural': 'پاتوق های گزارش شده',
                'ordering': ['patogh_id'],
                'unique_together': {('patogh_id', 'username')},
            },
        ),
    ]
