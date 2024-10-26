from django.urls import path

from . import views

app_name = "fileprocessor"

urlpatterns = [
    path("", views.upload_file, name="upload"),
    path("summary/<int:pk>/", views.summary_view, name="summary_view"),
]
