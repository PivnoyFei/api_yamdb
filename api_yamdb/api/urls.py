from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'users'

router = DefaultRouter()
router.register("users", views.UserViewSet, "users")

authentication = [
    path("signup/", views.get_signup),
    path("token/", views.get_token),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(authentication)),
]
