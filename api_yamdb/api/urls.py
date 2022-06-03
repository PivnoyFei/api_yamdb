from api import views
from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = 'api'

router = SimpleRouter()
router.register('users', views.UserViewSet, 'users')
router.register(r'genres', views.GenreViewSet, 'genres')
router.register(r'titles', views.TitleViewSet, 'titles')
router.register(r'categories', views.CategoryViewSet, 'categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, 'reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet, 'comments',
)

authentication = [
    path("signup/", views.get_signup),
    path("token/", views.get_token),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(authentication)),
]
