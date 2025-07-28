from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('createpost/', views.createpost, name='createpost'),
    path('postsconfig/', views.postsconfig, name='postsconfig'),
    path('editpost/<int:post_id>', views.editpost, name='editpost'),
]
