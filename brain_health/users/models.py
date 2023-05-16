from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from brain_health.users.managers import UserManager



class User(AbstractUser):
    name = models.CharField(_("Name of User"), max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='user_profiles/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_therapist = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def brain_health_score(self):
        ratings = self.brain_score.all()
        if ratings:
            return round(sum(r.rating for r in ratings) / len(ratings), 2)
        else:
            return 0


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Therapist(models.Model):
    user = models.OneToOneField(User, related_name="therapist_profile", on_delete=models.CASCADE)
    degrees = models.TextField(null=True, blank=True)
    certifications = models.TextField(null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def star(self):
        ratings = self.feedbacks.all()
        if ratings:
            return round(sum(r.rating for r in ratings) / len(ratings), 2)
        else:
            return 0


@receiver(post_save, sender=User)
def create_therapist_profile(sender, instance, created, **kwargs):
    if created and instance.is_therapist:
        Therapist.objects.create(user=instance)




class Feedback(models.Model):
    user = models.ForeignKey(User, related_name="feedbacks", on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, related_name="feedbacks", on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.name} - {self.user.email}"


class Brain_Health_Score(models.Model):
    user = models.ForeignKey(User, related_name="brain_score", on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.rating}"
