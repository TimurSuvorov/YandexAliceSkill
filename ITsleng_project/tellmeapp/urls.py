from django.urls import path

from .views import anchortellme

urlpatterns = [
    path('', anchortellme, name='anchortellme'),
]
