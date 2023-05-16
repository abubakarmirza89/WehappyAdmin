from django.urls import path

from brain_health.users.views import (
    CreateAppointmentViewSet,
    FeedbackCreateView,
    LoginAPIView,
    TherapistListViewSet,
    UserSignupView,
)

app_name = "users"

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="api-signup"),
    path("login/", LoginAPIView.as_view(), name="api-login"),
    path("therapists/", TherapistListViewSet.as_view(), name="api-therapist"),
    path("feedback/<int:pk>/", FeedbackCreateView.as_view(), name="api-feedback"),
    path("create-appointment/<int:pk>/", CreateAppointmentViewSet.as_view(), name="api-create-appointment"),
]
