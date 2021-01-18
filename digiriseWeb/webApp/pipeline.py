from social_django.utils import load_strategy


def get_oauth2_token(user):
    social = user.social_auth.get(provider='github')
    strategy = load_strategy()
    social.refresh_token(strategy)
    return social.extra_data['access_token']