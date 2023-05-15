from brain_health.health.api.views import (
    RelativeList,
    MoodListView,
    SuggestionByMoodView,
    SuggestionDetailView,
    MoodDetailView,
    )

from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter


app_name = "health"

urlpatterns = [
    path('moods/', MoodListView.as_view(), name='mood-list'),
    path('moods/<int:pk>/', MoodDetailView.as_view(), name='mood-detail'),
    path('suggestions/by-mood/', SuggestionByMoodView.as_view(), name='suggestion-by-mood'),
    path('suggestions/<int:pk>/', SuggestionDetailView.as_view(), name='suggestion-detail'),

]



if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("relative", RelativeList)


urlpatterns += router.urls
