from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register("users", views.UserViewSet, "users")

authentication = [
    path("signup/", views.SignUpViewSet.as_view()),
    path("token/", views.TokenViewSet.as_view()),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(router.urls)),
]
