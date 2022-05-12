import uuid

from django.contrib.auth import get_user_model

from accounts.models import UserProfile

User = get_user_model()


def bulk_create_user(number_of_user):
    for i in range(number_of_user):
        user = User.objects.create(
            username=f'test_user_{str(uuid.uuid4())[:8]}',
            password=str(uuid.uuid4())
        )
        UserProfile.objects.create(
            user=user,
            nickname=user.username,
            desc=user.username
        )
