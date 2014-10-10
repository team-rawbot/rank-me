def user_details(strategy, details, response, user=None, *args, **kwargs):
    user_profile = user.get_profile()
    user_profile.avatar = response['profile_image_url']
    user_profile.twitter = response['screen_name']
    user_profile.save()
