from django.db import models
from config.settings.base import AUTH_USER_MODEL
from brain_health.users.models import Therapist

User = AUTH_USER_MODEL

class Relative(models.Model):
    user = models.ForeignKey(User, related_name="relative", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    is_app_user = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Mood(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()

    def __str__(self):
        return self.name


class Suggestion(models.Model):
    mood = models.ForeignKey(Mood, related_name="suggestion", on_delete=models.CASCADE)
    suggestion_text = models.TextField()
    from_age = models.IntegerField()
    to_age = models.IntegerField()

    def __str__(self):
        return self.suggestion_text


class Message(models.Model):
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    message_text = models.TextField()
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return self.message_text


class Appointment(models.Model):
    user = models.ForeignKey(User, related_name="appointments", on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, related_name="appointments", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.therapist.name}"


class Feedback(models.Model):
    user = models.ForeignKey(User, related_name="feedbacks", on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, related_name="feedbacks", on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.therapist.name}"

