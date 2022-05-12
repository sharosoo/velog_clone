from django.contrib.auth import get_user_model

User = get_user_model()


def delete_all_user():
    user_queryset = User.objects.filter(is_superuser=False)
    for user in user_queryset:
        user.delete()
