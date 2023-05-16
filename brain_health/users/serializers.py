from django.contrib.auth import get_user_model
from rest_framework import serializers

from brain_health.users.models import Appointment, Feedback, Therapist

User = get_user_model()


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("rating", "comment")


class TherapistSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:therapist-detail", lookup_field="pk")
    create_feedback = serializers.HyperlinkedIdentityField(view_name="users:api-feedback", lookup_field="pk")
    create_appointment = serializers.HyperlinkedIdentityField(
        view_name="users:api-create-appointment", lookup_field="pk"
    )
    feedbacks = FeedbackSerializer(many=True)

    class Meta:
        model = Therapist
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail", lookup_field="pk")

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "brain_health_score",
            "profile_picture",
            "phone_number",
            "is_therapist",
            "url",
        ]

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        fields["therapist_profile"] = TherapistSerializer(read_only=True)
        return fields


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "password", "brain_health_score", "phone_number", "is_therapist"]

    def create(self, validated_data):
        email = validated_data.get("email")
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(**validated_data)
            return user
        else:
            raise serializers.ValidationError("Email already exists.")


class AppointmentTherapistSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:appointment-detail", lookup_field="pk")
    user_name = serializers.ReadOnlyField(source="user.name")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date = serializers.ReadOnlyField()
    time = serializers.ReadOnlyField()
    location = serializers.ReadOnlyField()
    reason = serializers.ReadOnlyField()

    class Meta:
        model = Appointment
        fields = (
            "id",
            "user_name",
            "date",
            "time",
            "location",
            "reason",
            "is_confirmed",
            "created_at",
            "url",
        )


class AppointmentUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:appointment-detail", lookup_field="pk")
    therapist_name = serializers.ReadOnlyField(source="therapist.user.name")

    class Meta:
        model = Appointment
        fields = (
            "id",
            "therapist_name",
            "date",
            "time",
            "location",
            "reason",
            "url",
        )
