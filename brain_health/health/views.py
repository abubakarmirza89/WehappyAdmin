from rest_framework import generics, mixins, viewsets
from rest_framework import permissions
from .tasks import send_email_task


from .serializers import (
    RelativeSerializer,
    MoodSerializer,
    SuggestionSerializer,
    AppointmentSerializer,
)
from brain_health.health.models import (
    Relative,
    Appointment,
    Suggestion,
    Message,
    Mood,
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



class SuggestionByMoodView(generics.ListAPIView):
    serializer_class = SuggestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        mood_name = self.request.query_params.get('mood')
        mood = Mood.objects.filter(name__iexact=mood_name).first()
        if not mood:
            return Suggestion.objects.none()

        suggestions = Suggestion.objects.filter(mood=mood).order_by('?')
        if not suggestions.exists():
            return Suggestion.objects.none()

        message = Message.objects.filter(mood=mood).order_by('?').first()
        if message:
            suggestion_text = suggestions.first().suggestion_text
            message_text = message.message_text
            is_urgent = message.is_urgent
            user = self.request.user
            relatives = Relative.objects.filter(user=user)
            for relative in relatives:
                message_body = f"Hey {relative.name}, {user.name} has been feeling {mood.name.lower()}. Here's a suggestion: {suggestion_text}\n\n{message_text}\n\nIs urgent: {is_urgent}\n\nThanks,"
                send_email_task.delay('Mood', message_body, [relative.email])

        return suggestions
