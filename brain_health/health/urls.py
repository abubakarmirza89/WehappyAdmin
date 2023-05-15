from brain_health.health.views import (
    RelativeList,
    MoodListView,
    SuggestionByMoodView,
    )

from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter


app_name = "health"

urlpatterns = [
    path('moods/', MoodListView.as_view(), name='mood-list'),
    path('suggestions/by-mood/', SuggestionByMoodView.as_view(), name='suggestion-by-mood'),

]



if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("relative", RelativeList)


urlpatterns += router.urls
