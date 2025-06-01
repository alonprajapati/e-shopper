from django.urls import path
from .views import *

urlpatterns = [
    path("initkhalti/<int:id>",initkhalti,name="initkhalti"),
    path("verify/",verifyKhalti,name="verify"),
]
