from django.db import models
from config.settings.base import AUTH_USER_MODEL


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
    description = models.TextField()

    def __str__(self):
        return self.name


class Suggestion(models.Model):
    mood = models.ForeignKey(Mood, related_name="suggestion", on_delete=models.CASCADE)
    suggestion_text = models.TextField()
    is_specific_to_age_group = models.BooleanField(default=False)
    is_specific_to_gender = models.BooleanField(default=False)

    def __str__(self):
        return self.suggestion_text


class Message(models.Model):
    relative = models.ForeignKey(Relative, related_name="message", on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    message_text = models.TextField()
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return self.message_text




class Therapist(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='therapist_profiles/')
    degrees = models.TextField()
    certifications = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    user = models.ForeignKey(User, related_name="appointment", on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, related_name="appointment_therapist", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.name} - {self.therapist.name}"

