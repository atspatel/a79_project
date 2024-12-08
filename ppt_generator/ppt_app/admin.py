# ppt_app/admin.py
from django.contrib import admin
from .models import Presentation, PresentationSlide
from utils.json_utils import BaseJsonAdmin


class PresentationAdmin(BaseJsonAdmin):
    list_display = (
        "id",
        "user",
        "topic",
        "description",
        "num_slides",
        "status",
        "create_time",
        "update_time",
        "is_active",
    )
    search_fields = (
        "topic",
        "description",
        "user__email",
    )
    list_filter = ["status"]


admin.site.register(Presentation, PresentationAdmin)


class PresentationSlideAdmin(BaseJsonAdmin):
    list_display = ("presentation", "index", "layout_id")
    list_filter = ("presentation",)
    search_fields = ("presentation__name", "layout_name", "content")


# Register the admin class with the PresentationSlide model
admin.site.register(PresentationSlide, PresentationSlideAdmin)
