from .models import UserProfile


def user_details(strategy, details, response, user=None, *args, **kwargs):
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    user_profile.avatar = response['profile_image_url']
    user_profile.twitter = response['screen_name']
    user_profile.save()
