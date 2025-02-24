from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="team_leader")
    members = models.ManyToManyField(User, related_name="teams", blank=True)
    total_campaigns = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    
class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50,null=True)


    def __str__(self):
        return f"{self.name} ({self.email})-{self.department}"    
    
# Automatically create a Profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
