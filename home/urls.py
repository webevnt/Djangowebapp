from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:operation>/<int:pk>/', views.change_friends, name='change_friends'),
    path('post_details/<int:pk>', views.add_comment_to_post, name='add_comment_to_post'),
    path('delete/<int:pk>', views.delete_my_comment,name='delete_my_comment'),
    path('mydelete/<int:id>',views.deletemypost,name="del post")
]

