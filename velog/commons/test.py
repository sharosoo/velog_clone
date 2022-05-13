import uuid

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone


from recommends.models import (
    RecommendToday,
    RecommendWeekly,
    RecommendMonthly
)
from likes.models import Like
from articles.models import Article
from accounts.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

FROZEN_TIME_BASE = timezone.now()
FROZEN_TIME = FROZEN_TIME_BASE.strftime("%Y%m%dT%H:%M:%S")
FROZEN_TIME_WEEK_AGO = (FROZEN_TIME_BASE + relativedelta(weeks=-1)).strftime("%Y%m%dT%H:%M:%S")
FROZEN_TIME_MONTH_AGO = (FROZEN_TIME_BASE + relativedelta(months=-1)).strftime("%Y%m%dT%H:%M:%S")


def get_users(iteration):
    users = list()
    for _ in range(iteration):
        user = User.objects.create(username=f'user_{str(uuid.uuid4())[:8]}')
        users.append(user)

    return users


def get_profiles(iteration):
    profiles = list()
    for user in get_users(iteration):
        profile = UserProfile.objects.create(
            nickname=user.username,
            user=user,
            desc=user.username
        )
        profiles.append(profile)

    return profiles


def get_articles(profile, iteration):
    articles = list()
    for i in range(iteration):
        article = Article.objects.create(
            profile=profile,
            title=f'{profile.nickname}{str(uuid.uuid4())[:8]}',
            slug=f'{profile.nickname}{str(uuid.uuid4())[:8]}',
            content=f'{profile.nickname}{str(uuid.uuid4())[:8]}'
        )
        articles.append(article)

    return articles


def drf_strftime(obj):
    return obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def nested_drf_strftime(obj):
    return drf_strftime(obj)[:-4] + 'Z'
