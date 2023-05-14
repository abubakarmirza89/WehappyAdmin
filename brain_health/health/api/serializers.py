from rest_framework import serializers
from brain_health.health.models import (
    Relative,
    Appointment,
    Suggestion,
    Message,
    Mood,
    Therapist
)


class RelativeSerializer(serializers.ModelSerializer):
    model = Relative
    fields = [
        "user",
        "name",
        "email",
        "phone_number",
        "is_app_user"
    ]


class MoodSerializer(serializers.ModelSerializer):
    model = Mood
    fields = [
        "user",
        "score",
        "description",

    ]

class SuggestionSerializer(serializers.ModelSerializer):
    model = Suggestion
    fields = [
        "mood",
        "suggestion_text",
        "is_specific_to_age_group",
        "is_specific_to_gender",
    ]

class MessageSerializer(serializers.ModelSerializer):
    model = Message
    fields = [
        "relative",
        "mood",
        "message_text",
        "is_urgent",
    ]



class TherapistSerializer(serializers.ModelSerializer):
    model = Therapist
    fields = [
        "name",
        "email",
        "phone_number",
        "profile_picture",
        "degrees"
        "certifications"
        "hourly_rate"
        "is_available"
    ]

class AppointmentSerializer(serializers.ModelSerializer):
    model = Appointment
    fields = [
        "user",
        "therapist",
        "date",
        "time",
        "location"
        "reason"
    ]
