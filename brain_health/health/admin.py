from django.contrib import admin


from brain_health.health.models import (
    Relative,
    Appointment,
    Suggestion,
    Message,
    Mood,
    Therapist,
)

@admin.register(Relative)
class RelativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'is_app_user')
    list_filter = ('is_app_user',)
    search_fields = ('name', 'email', 'phone_number')


class SuggestionAdmin(admin.StackedInline):
    model = Suggestion
    extra = 1

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'score')
    inlines = [SuggestionAdmin]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_text', 'relative', 'mood', 'is_urgent')
    list_filter = ('is_urgent',)

class AppointmentAdmin(admin.StackedInline):
    model = Appointment
    extra = 1

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'hourly_rate', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'email', 'phone_number')
    inlines = [AppointmentAdmin]



