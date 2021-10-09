import hashlib

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver

from allauth.account.signals import user_signed_up


class MyUserManager(UserManager):
    """
    Custom User Model manager.

    It overrides default User Model manager's create_user() and create_superuser,
    which requires username field.
    """

    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True,
                          is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User instances represent a user on this site.

    Important: You don't have to use a custom user model. I did it here because
    I didn't want a username to be part of the system and I wanted other data
    to be part of the user and not in a separate table. 

    You can avoid the username issue without writing a custom model but it
    becomes increasingly obtuse as time goes on. Write a custom user model, then
    add a custom admin form and model.

    Remember to change ``AUTH_USER_MODEL`` in ``settings.py``.
    """

    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(
        _('first name'), max_length=40, blank=True, null=True, unique=False)
    last_name = models.CharField(
        _('last name'), max_length=40, blank=True, null=True, unique=False)
    display_name = models.CharField(
        _('display name'), max_length=14, blank=True, null=True, unique=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserProfile(models.Model):
    """Profile data about a user.
    Certain data makes sense to be in the User model itself, but some
    is more "profile" data than "user" data. I think this is things like
    date-of-birth, favourite colour, etc. If you have domain-specific
    profile information you might create additional profile classes, like
    say UserGeologistProfile.
    """
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile',
                                on_delete=models.CASCADE)

    # I oscillate between whether the ``avatar_url`` should be
    # a) in the User model
    # b) in this UserProfile model
    # c) in a table of it's own to track multiple pictures, with the
    #    "current" avatar as a foreign key in User or UserProfile.
    avatar_url = models.CharField(max_length=256, blank=True, null=True)


@receiver(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):
    """
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:

    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']

    See the socialaccount_socialaccount table for more in the 'extra_data' field.

    From http://birdhouse.org/blog/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/comment-page-1/
    """

    if sociallogin:

        if sociallogin.account.provider == 'facebook':
            user_data = user.socialaccount_set.filter(
                provider='facebook')[0].extra_data
            print(user_data)
            picture_url = user_data['picture']['data']['url']
            user.first_name = sociallogin.account.extra_data['first_name']
            user.last_name = sociallogin.account.extra_data['last_name']

    profile = UserProfile(user=user, avatar_url=picture_url)
    profile.save()

    user.save()
