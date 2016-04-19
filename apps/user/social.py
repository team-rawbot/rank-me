from .models import UserProfile


def user_details(strategy, details, response, user=None, *args, **kwargs):
    # The Twitter image URL looks like ..._normal.jpg, to get the full-size
    # image we need to remove the _normal part
    profile_image_url = (
        response['profile_image_url'].replace('_normal.', '.')
                                     .replace('http:', 'https:')
    )

    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    user_profile.avatar = profile_image_url
    user_profile.twitter = response['screen_name']
    user_profile.save()
