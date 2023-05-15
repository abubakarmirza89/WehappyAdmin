from rest_framework import generics, mixins, viewsets
from rest_framework import permissions
from django.core.mail import send_mail
from django.conf import settings

Email = settings.DEFAULT_FROM_EMAIL

from .serializers import (
    RelativeSerializer,
    MoodSerializer,
    SuggestionSerializer,
    MessageSerializer,
    TherapistSerializer,
    AppointmentSerializer,
)
from brain_health.health.models import (
    Relative,
    Appointment,
    Suggestion,
    Message,
    Mood,
    Therapist
)

class RelativeList(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):

    serializer_class = RelativeSerializer
    queryset = Relative.objects.all()
    permission_class = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return Relative.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





class MoodListView(generics.ListAPIView):
    serializer_class = MoodSerializer
    queryset = Mood.objects.all()
    permission_class = [permissions.IsAuthenticated]


class MoodDetailView(generics.RetrieveAPIView):
    serializer_class = MoodSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Mood.objects.all()



class SuggestionByMoodView(generics.ListAPIView):
    serializer_class = SuggestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        mood_name = self.request.query_params.get('mood')
        mood = Mood.objects.filter(name__iexact=mood_name).first()
        if mood:
            suggestion = Suggestion.objects.filter(mood=mood)
            message = Message.objects.filter(mood=mood)
            if suggestion.exists():
                user = self.request.user
                message = f"{user.name} He Is {mood} {message[0].message_text}"
                send_mail('Mood',message, settings.DEFAULT_FROM_EMAIL, ['brainhealth@example.com'],)
            return suggestion
        else:
            return Suggestion.objects.none()


class SuggestionDetailView(generics.RetrieveAPIView):
    serializer_class = SuggestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Suggestion.objects.all()




