from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from brain_health.users.models import Appointment, Feedback, Therapist

from .serializers import (
    AppointmentTherapistSerializer,
    AppointmentUserSerializer,
    FeedbackSerializer,
    LoginSerializer,
    TherapistSerializer,
    UserSerializer,
    UserSignupSerializer,
)

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_class = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            try:
                return self.queryset.get(id=self.request.user.id)
            except User.DoesNotExist:
                pass
        else:
            return self.queryset.all()

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_class = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"success": "login successfully", "token": token.key, "user": LoginSerializer(user).data},
            status=status.HTTP_200_OK,
        )


class UserSignupView(CreateAPIView):
    model = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_class = [AllowAny]


class TherapistListViewSet(ListAPIView):
    serializer_class = TherapistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Therapist.objects.filter(is_available=True)


class TherapistDetailViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = TherapistSerializer
    queryset = Therapist.objects.all()
    permission_class = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return Therapist.objects.filter(user=self.request.user)


class FeedbackCreateView(CreateAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_class = [IsAuthenticated]
    lookup_field = "pk"

    def perform_create(self, serializer):
        therapist_id = self.kwargs.get("pk")
        therapist = Therapist.objects.get(pk=therapist_id)
        serializer.save(user=self.request.user, therapist=therapist)


class AppointmentViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Appointment.objects.all()
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_therapist:
            therapist = Therapist.objects.get(user=user)
            return Appointment.objects.filter(therapist=therapist)
        else:
            return Appointment.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.user.is_therapist:
            return AppointmentTherapistSerializer
        else:
            return AppointmentUserSerializer


class CreateAppointmentViewSet(CreateAPIView):
    serializer_class = AppointmentUserSerializer
    queryset = Appointment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        appointment_id = self.kwargs.get("pk")
        therapist = Therapist.objects.get(pk=appointment_id)
        serializer.save(user=user, therapist=therapist)
