from django.urls import path

from .views import anchorhandler

urlpatterns = [
    path('', anchorhandler, name='simpleresponse'),
]
