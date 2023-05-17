from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from brain_health.users.views import AppointmentViewSet, NotificationViewSet, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("appointment", AppointmentViewSet)
router.register("notifications", NotificationViewSet, basename="notification")


app_name = "api"
urlpatterns = router.urls
