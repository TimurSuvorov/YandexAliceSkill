from django.urls import path

from .views import anchorlistenit

urlpatterns = [
    path('', anchorlistenit, name='anchorlistenit'),
]