from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet, CommentsViewSet
from users.views import SignUpViewSet, TokenViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
    path('v1/auth/token/', TokenViewSet.as_view(), name='token'),
    path("v1/", include(router.urls)),
]
