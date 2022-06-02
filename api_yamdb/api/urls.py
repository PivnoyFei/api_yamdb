from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = 'users'

router = DefaultRouter()
router.register('users', views.UserViewSet, 'users')
router.register("titles", views.TitleViewSet, "title")
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet,
    basename='comments'
)

authentication = [
    path("signup/", views.get_signup),
    path("token/", views.get_token),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(authentication)),
]
