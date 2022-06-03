from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import ReviewViewSet, CommentsViewSet
from api.views import UserViewSet, GenreViewSet, CategoryViewSet, TitleViewSet

from api.views import get_token, get_signup

app_name = 'api'

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,

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
    CommentsViewSet,
    basename='comments',
)

authentication = [
    path("signup/", views.get_signup),
    path("token/", views.get_token),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(authentication)),
]
