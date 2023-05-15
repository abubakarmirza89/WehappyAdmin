from brain_health.users.views import UserSignupView, LoginAPIView, TherapistListViewSet, FeedbackCreateView
from django.urls import path

app_name = "users"

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="api-signup"),
    path("login/", LoginAPIView.as_view(), name="api-login"),
    path("therapists/", TherapistListViewSet.as_view(), name="api-therapist"),
    path("feedback/<int:pk>/", FeedbackCreateView.as_view(), name="api-feedback"),

]
