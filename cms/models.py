from django.contrib.auth.base_user import (
    AbstractBaseUser, BaseUserManager,
)
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# User-related
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    email = models.EmailField(_('email address'), unique=True)

    GRADE_CHOICES = [
        ('B1', '学士1年'),
        ('B2', '学士2年'),
        ('B3', '学士3年'),
        ('B4', '学士4年'),
        ('Mr', '修士'),
        ('Dr', '博士'),
    ]
    grade = models.CharField(_('学年'), max_length=3, choices=GRADE_CHOICES, blank=True)
    twitter = models.CharField(_('Twitter'), max_length=50, blank=True)
    github = models.CharField(_('GitHub'), max_length=50, blank=True)
    bio = models.TextField(
        _('自己紹介'),
        help_text=_('必須。140字以内。'),
        max_length=140,
        blank=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


# Project-related
class Tag(models.Model):
    name = models.CharField(_('タグ'), max_length=50)

    def __str__(self):
        if hasattr(self, 'note_count'):
            return f'{self.name}({self.note_count})'
        return self.name


class Project(models.Model):
    name = models.CharField(_('プロジェクト名'), max_length=50, unique=True)

    # tag = models.ManyToManyField(Tag)
    members = models.ManyToManyField(User, through='ProjectUserRelation')

    twitter = models.CharField(_('Twitter'), max_length=50, blank=True)
    github = models.CharField(_('GitHub'), max_length=50, blank=True)
    product_url = models.URLField(
        _('プロダクトURL'),
        help_text=_('必須。まだ完成していない場合ピッチ資料のGoogle Driveリンクなどを与えること。')
    )
    description = models.TextField(
        _('プロダクト説明'),
        help_text=_('必須。140字以内。'),
        max_length=140
    )

    STATE_CHOICES = [
        ('0', 'Dead'),
        ('1', 'Idea'),
        ('2', 'Prototyping'),
        ('3', 'Launched'),
        ('4', 'User-acquired'),
    ]
    state = models.CharField(
        _('プロジェクトのレベル'),
        max_length=2,
        choices=STATE_CHOICES,
        default='1',
    )

    does_accept_application = models.BooleanField(_('メンバーを募集しているかどうか'), default=False)
    application = models.TextField(_('応募方法'), blank=True)

    is_public = models.BooleanField(_('公開可能かどうか'), default=True)
    created_at = models.DateTimeField(_('プロジェクト作成日'), default=timezone.now)
    updated_at = models.DateTimeField(_('プロジェクト更新日'), auto_now=True)

    def __str__(self):
        return self.name


class ProjectUserRelation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)


class ProjectLog(models.Model):
    title = models.CharField(_('ログタイトル'), max_length=50)
    text = models.TextField(_('ログ内容'))
    achievement = models.PositiveSmallIntegerField(
        _('達成度'),
        validators = [MinValueValidator(0), MaxValueValidator(10)],
        help_text=_('必須。10段階で達成度を評価してください。'),
    )
    created_at = models.DateTimeField(_('ログ作成日'), default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)


class ProjectPlan(models.Model):
    content = models.CharField(_('プラン内容'), max_length=255)
    date = models.DateField(_('プラン期日'))
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
