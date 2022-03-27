from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default= 18)
    city = models.CharField(max_length=150, blank=True, verbose_name='город')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)),null=True)

    @property
    def is_activation_key_expired(self):
        try:
            if now() <= self.activation_key_expires:
                return False
        except Exception as e:
            pass
        return True


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'Male'),  # (What we save in the DB, How it is shown )
        (FEMALE, 'Female'),
    )

    user = models.OneToOneField(ShopUser,null=False, db_index=True, on_delete=models.CASCADE)
    about = models.TextField(verbose_name='About yourself', blank=True,null=True)
    gender = models.CharField(verbose_name='Sex',choices=GENDER_CHOICES,blank=True,max_length=2)


@receiver(post_save, sender = ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=ShopUser)
def save_user_profile(sender,instance, **kwargs):
    instance.userprofile.save()
