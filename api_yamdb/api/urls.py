from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register("titls", views.ReviewViewSet, "titls")


urlpatterns = [
    path("v1/", include(router.urls)),
]
