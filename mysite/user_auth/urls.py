from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import *

app_name = 'user_auth'

urlpatterns = [
    # login logout
    path(
        'login/',
        LoginPkView.as_view(
            template_name='user_auth/login.html',
            redirect_authenticated_user=True,
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(
            next_page=reverse_lazy('user_auth:login')
        ),
        name='logout'
    ),

    # для проверки интернационализации
    path('h/', HelloView.as_view(), name='hello'),

    # user: create, info, update
    path('new/', CreateUserView.as_view(), name='create_user'),
    path('<int:pk>/', ShowUserInfoView.as_view(), name='user_info'),
    path('<int:pk>/update-user/', UpdateUserView.as_view(), name='update_user'),

    # profile: create, update
    path('<int:pk>/create-profile/', CreateProfileView.as_view(), name='create_profile'),
    path('<int:pk>/update-profile/', UpdateProfileView.as_view(), name='update_profile'),

    path('redirect/', redirect_for_logged_user, name='redirect_for_logged_user')
]
