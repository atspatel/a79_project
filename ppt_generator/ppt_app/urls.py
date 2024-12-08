# ppt_app/urls.py
from django.urls import path
from .views import PresentationView, PresentationDownloadView

urlpatterns = [
    path(
        "presentations/", PresentationView.as_view(), name="presentation-create"
    ),  # POST
    path(
        "presentations/<uuid:id>/",
        PresentationView.as_view(),
        name="presentation-detail",
    ),  # GET, PUT
    path(
        "presentations/<uuid:id>/download",
        PresentationDownloadView.as_view(),
        name="presentation-download",
    ),
]
