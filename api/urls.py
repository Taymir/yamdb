from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('titles', views.TitlesViewSet)
router.register('genres', views.GenreViewSet)
router.register('categories', views.CategoryViewSet)


urlpatterns = [
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/email/', views.send_email_confirmation, name='send_email_confirmation'),
    path('auth/token/', views.confirm_email, name='confirm_email'),
    path('', include(router.urls)),
]
