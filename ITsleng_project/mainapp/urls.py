from django.urls import path

from .views import anchorhandler, echo

urlpatterns = [
    path('', anchorhandler, name='simpleresponse'),
    path('echo/', echo)
]