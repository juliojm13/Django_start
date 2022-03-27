from django.core.management.base import BaseCommand

from authapp.models import ShopUser, UserProfile

class Command(BaseCommand):
    def handle(self, *args, **options):
        exclude_user_idx = UserProfile.objects.only('user').values_list('user__id', flat=True)
        users = ShopUser.objects.exclude(id__in = exclude_user_idx).only('id')
        if users.exists():
            create_profiles = [UserProfile(user=user) for user in users]
            UserProfile.objects.bulk_create(create_profiles)