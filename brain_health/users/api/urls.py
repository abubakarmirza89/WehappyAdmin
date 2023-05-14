from brain_health.users.api.views import UserSignupView, LoginAPIView
from django.urls import path

app_name = "users"

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="api-signup"),
    path("login/", LoginAPIView.as_view(), name="api-login"),

]
