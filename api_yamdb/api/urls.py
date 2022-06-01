from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'users'

router = DefaultRouter()
router.register("users", views.UserViewSet, "users")

authentication = [
    #path("signup/", views.SignUpViewSet.as_view()),
    #path("token/", views.TokenViewSet.as_view()),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", views.get_confirmation_code),
    path("v1/auth/token/", views.get_token),
]