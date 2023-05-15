from django.contrib.auth import get_user_model
from rest_framework import serializers
from brain_health.users.models import Therapist, Feedback

User = get_user_model()


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('rating', 'comment')


class TherapistSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:therapist-detail", lookup_field="pk")
    feedbacks = FeedbackSerializer(many=True)
    create_feedback = serializers.HyperlinkedIdentityField(view_name="users:api-feedback", lookup_field="pk")

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
        user = self.context["request"].user

        if user.is_authenticated and user.is_therapist:
            fields["therapist_profile"] = TherapistSerializer(read_only=True)

        return fields


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            'password',
            "brain_health_score",
            "phone_number",
            "is_therapist"
            ]

    def create(self, validated_data):
        email = validated_data.get("email")
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(**validated_data)
            return user
        else:
            raise serializers.ValidationError("Email already exists.")


