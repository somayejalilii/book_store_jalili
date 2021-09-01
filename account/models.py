from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


# Create your models here.


class BaseUser(AbstractBaseUser, PermissionsMixin):
# class BaseUser(AbstractBaseUser):
    """
    a custom user model for authentication
    """
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField("email address", unique=True)
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
    # slug = AutoSlugField(populate_from=['username'], unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    # mobile = models.CharField(max_length=13, unique=True)
    # key = models.CharField(max_length=100, null=True, blank=True, editable=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    """
    A string describing the name of the field on the user model that is used as the unique identifier
    """
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def full_name(self):
        return self.get_full_name()


class Admin(BaseUser):
    class Meta:
        proxy = True
        verbose_name = 'admin'
        verbose_name_plural = 'admins'


class Customer(BaseUser):
    class Meta:
        proxy = True
        verbose_name = 'customer'
        verbose_name_plural = 'customers'


class Employee(BaseUser):
    class Meta:
        proxy = True
        verbose_name = 'employee'
        verbose_name_plural = 'employees'


class Address(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='ads')
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    postal_code = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/', null=True,blank=True)

    def __str__(self):
        return self.user.username

def save_profile_user(sender, **kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user, sender=BaseUser)
