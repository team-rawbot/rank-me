def user_details(strategy, details, response, user=None, *args, **kwargs):
    details['avatar'] = response['profile_image_url']

    return {
        'details': details
    }
