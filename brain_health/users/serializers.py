from django.contrib.auth import get_user_model
from rest_framework import serializers

from brain_health.users.models import Appointment, Feedback, Therapist

User = get_user_model()


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("rating", "comment")


class TherapistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapist
        fields = (
            "degrees",
            "certifications",
            "card_id",
            "hourly_rate",
            "is_available",
        )
        extra_kwargs = {
            "degrees": {"required": False},
            "certifications": {"required": False},
            "card_id": {"required": False},
            "hourly_rate": {"required": False},
            "is_available": {"required": False},
        }


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail", lookup_field="pk")
    create_feedback = serializers.HyperlinkedIdentityField(
        view_name="users:api-feedback", lookup_field="pk", read_only=True
    )
    create_appointment = serializers.HyperlinkedIdentityField(
        view_name="users:api-create-appointment", lookup_field="pk", read_only=True
    )
    therapist_profile = TherapistProfileSerializer(required=False)
    feedback_therapist = FeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "profile_picture",
            "phone_number",
            "date_of_birth",
            "url",
            "create_feedback",
            "create_appointment",
            "therapist_profile",
            "feedback_therapist",
        )

    def to_representation(self, instance):
        if not instance.is_therapist:
            self.fields.pop("create_feedback")
            self.fields.pop("create_appointment")
            self.fields.pop("feedback_therapist")
            self.fields.pop("therapist_profile")

        return super().to_representation(instance)

    def update(self, instance, validated_data):
        therapist_profile_data = validated_data.pop("therapist_profile", None)
        instance = super().update(instance, validated_data)

        if therapist_profile_data and instance.is_therapist:
            therapist_profile_serializer = self.fields["therapist_profile"]
            therapist_profile_instance = instance.therapist_profile

            therapist_profile_serializer.update(therapist_profile_instance, therapist_profile_data)

        return instance


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
