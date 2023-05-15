from rest_framework import serializers
from brain_health.health.models import Relative, Appointment, Suggestion, Message, Mood


class RelativeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="health:relative-detail", lookup_field="pk")

    class Meta:
        model = Relative
        fields = "__all__"
        read_only_fields = ["id", "url"]


class MoodSerializer(serializers.ModelSerializer):
    suggestion = serializers.SerializerMethodField()

    class Meta:
        model = Mood
        fields = "__all__"

    def get_suggestion(self, obj):
        suggestions = obj.suggestion.all().values_list("suggestion_text", flat=True)
        return suggestions


class SuggestionSerializer(serializers.ModelSerializer):
    mood_name = serializers.ReadOnlyField(source='mood.name')

    class Meta:
        model = Suggestion
        fields = "__all__"


# class MessageSerializer(serializers.ModelSerializer):
#     relative_name = serializers.ReadOnlyField(source='relative.name')
#     mood_name = serializers.ReadOnlyField(source='mood.name')

#     class Meta:
#         model = Message
#         fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    therapist_name = serializers.ReadOnlyField(source='therapist.name')
    user_name = serializers.ReadOnlyField(source='user.first_name')

    class Meta:
        model = Appointment
        fields = "__all__"
