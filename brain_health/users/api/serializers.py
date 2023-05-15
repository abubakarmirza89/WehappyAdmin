from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


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
                "url"
                ]



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["name", "email",'password', "brain_health_score", "phone_number"]

    def create(self, validated_data):
        email = validated_data.get("email")
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(**validated_data)
            return user
        else:
            raise serializers.ValidationError("Email already exists.")
