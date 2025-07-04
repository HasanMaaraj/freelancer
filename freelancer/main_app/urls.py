from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='users-profile'),
    path('profile/edit', views.edit_profile, name='profiles_edit'),
    path('profile/<int:user_id>', views.view_profile, name='profiles_detail'),
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/create', views.create_job, name='jobs_create'),
    path('jobs/<int:pk>', views.jobs_detail, name='jobs_detail'),
    path('jobs/<int:pk>/delete', views.jobs_delete, name='jobs_delete'),
    path('jobs/<int:pk>/send-request', views.send_request, name='send_request'),
    path('jobs/<int:pk>/delete-request', views.delete_request, name='delete_request'),
    path('requests/<int:pk>/accept', views.accept_request, name='accept_request'),
    path('requests/<int:pk>/decline', views.decline_request, name='decline_request'),
    path('upload/<int:pk>', views.upload, name='upload'),
    path('download/<int:pk>', views.download, name='download'),
    path('notifications/<int:pk>', views.notifications, name='notifications')
]