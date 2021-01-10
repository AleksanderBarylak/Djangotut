from django.contrib import admin
from .models import tutorial, TutorialSeries, TutorialCategory
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.


class tutorialAdmin(admin.ModelAdmin):
        fieldsets = [
        ("Title/date",{"fields": ["tutorial_title","tutorial_published"]}),
        ("Content", {"fields": ["tutorial_content"]}),
        ("URL",{"fields": ["tutorial_slug"]}),
        ("Series",{"fields": ["tutorial_series"]})
    ]
        formfield_overrides = {
            models.TextField: {'widget': TinyMCE()}
            }

admin.site.register(TutorialSeries)
admin.site.register(TutorialCategory)
admin.site.register(tutorial,tutorialAdmin)
