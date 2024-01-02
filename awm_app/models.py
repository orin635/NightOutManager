from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    groupCode = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username} at ({self.lat}, {self.lon}) at {self.timestamp} gc : {self.groupCode}"


class Group(models.Model):
    groupCode = models.CharField(max_length=255, primary_key=True)
    pubNames = ArrayField(models.CharField(max_length=255), blank=True, null=True)
