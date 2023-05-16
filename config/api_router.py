from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from brain_health.users.views import AppointmentViewSet, TherapistDetailViewSet, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("therapist", TherapistDetailViewSet)
router.register("appointment", AppointmentViewSet)


app_name = "api"
urlpatterns = router.urls
