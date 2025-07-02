from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='users-profile'),
    path('profile/<int:pk>/update/', views.UserUpdate.as_view(), name='profiles_update'),
    path('profile/<int:user_id>', views.view_profile, name='profiles_detail'),
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/create', views.create_job, name='jobs_create'),
    path('jobs/<int:pk>', views.jobs_detail, name='jobs_detail'),
    path('jobs/<int:pk>/delete', views.jobs_delete, name='jobs_delete'),
    path('jobs/<int:pk>/send-request', views.send_request, name='send_request'),
    path('jobs/<int:pk>/delete-request', views.delete_request, name='delete_request'),
]