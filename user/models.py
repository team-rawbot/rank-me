from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    avatar = models.CharField(max_length=255, blank=True)

    def full_name(self):
        full_name = "%s %s" % (self.user.first_name, self.user.last_name)

        if not full_name.strip():
            display_name = self.user.username
        else:
            display_name = full_name

        return display_name.title()



@receiver(post_init, sender=User)
def user_post_init(sender, instance, **kwargs):
    """
    https://gist.github.com/troolee/1140516
    """
    def get_profile():
        user = instance
        if not hasattr(user, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable('You need to set AUTH_PROFILE_MODULE in your project settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable('app_label and model_name should be separated by a dot in the AUTH_PROFILE_MODULE setting')

            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable('Unable to load the profile model, check AUTH_PROFILE_MODULE in your project settings')
                user._profile_cache, _ = model._default_manager.using(user._state.db).get_or_create(user=user)
                user._profile_cache.user = user
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return user._profile_cache

    instance.get_profile = get_profile
