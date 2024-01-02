from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def new_user_created(sender, instance, created, **kwargs):
    print("New User Called")
    if created:
        print("It was a create")
        Profile.objects.create(user=instance, lat=53.347523, lon=-6.259261)



