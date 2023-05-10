from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('titles', views.TitlesViewSet)
router.register('genres', views.GenreViewSet)
router.register('categories', views.CategoryViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet)


urlpatterns = [
    path('auth/email/',
         views.send_email_confirmation, name='send_email_confirmation'),
    path('auth/token/',
         views.confirm_email, name='confirm_email'),
    path('', include(router.urls)),
]
