from django.conf.urls import url
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import usersListView, userView, CustomLoginView


urlpatterns = [
    url('users/', usersListView.as_view(), name='users'),
    url('user/(?P<pk>\d+)', userView.as_view(), name='user'),
    url('user/login', CustomLoginView.as_view(), name='custom_login'),

    # jwt urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]