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
    url = serializers.HyperlinkedIdentityField(view_name="health:relative-detail", lookup_field="pk")

    class Meta:
        model = Relative
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "is_app_user",
            "url",
        ]



class MoodSerializer(serializers.ModelSerializer):
    suggestion = serializers.SlugRelatedField(many=True, read_only=True, slug_field='suggestion_text')
    url = serializers.HyperlinkedIdentityField(view_name="health:mood-detail", lookup_field="pk")


    class Meta:
        model = Mood
        fields = [
            "id",
            "name",
            "score",
            "url",
            "suggestion",

        ]

class SuggestionSerializer(serializers.ModelSerializer):
    mood_name = serializers.ReadOnlyField(source='mood.name')

    class Meta:
        model = Suggestion
        fields = ('id', 'mood', 'mood_name',
                'suggestion_text', 'from_age', 'to_age')


class MessageSerializer(serializers.ModelSerializer):
    relative_name = serializers.ReadOnlyField(source='relative.name')
    mood_name = serializers.ReadOnlyField(source='mood.name')

    class Meta:
        model = Message
        fields = ('id', 'relative', 'relative_name', 'mood',
                'mood_name', 'message_text', 'is_urgent')


class TherapistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapist
        fields = ('id', 'name', 'email', 'phone_number',
                'profile_picture', 'degrees', 'certifications', 'hourly_rate', 'is_available')


class AppointmentSerializer(serializers.ModelSerializer):
    therapist_name = serializers.ReadOnlyField(source='therapist.name')
    user_name = serializers.ReadOnlyField(source='user.first_name')

    class Meta:
        model = Appointment
        fields = ('id', 'user', 'user_name', 'therapist',
                'therapist_name', 'date', 'time', 'location', 'reason')
