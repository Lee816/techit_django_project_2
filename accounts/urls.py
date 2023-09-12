from django.urls import path

from . import views

app_name='accounts'
urlpatterns = [
    path('register/',views.RegisterUser, name='register'),
    path('login/',views.LoginUser, name='login'),
    path('logout/',views.LogoutUser, name='logout'),
    path('update/',views.UpdateUser, name='update'),
    path('changePW/',views.ChangePWUser, name='changePW'),
]
