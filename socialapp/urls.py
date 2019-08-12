from django.urls import path
from . import views
app_name = 'socialapp'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('profile/<int:id>', views.view_profile, name='profile'),
]