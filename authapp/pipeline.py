from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone

from authapp.models import UserProfile
from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    # api_url = urlunparse(('https', 'api.vk.com', '/method/users.get', None,
    #                       urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
    #                                             access_token=response['access_token'], v='5.131')), None))

    # api_url easier
    fields = ','.join(('sex', 'about', 'bdate', 'photo'))
    version = '5.131'
    access_token = response['access_token']
    # print(access_token)
    api_url = f'http://api.vk.com/method/users.get?fields={fields}&access_token={access_token}&v={version}'
    resp = requests.get(api_url)

    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]
    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    else:
        pass
    if data['about']:
        user.userprofile.about = data['about']
    if data['photo']:
        photo = data['photo']
    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year
    user.age = age
    user.avatar = photo
    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    user.save()
