from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='users-profile'),
    path('profile/<int:pk>/update/', views.UserUpdate.as_view(), name='profiles_update'),
    path('profile/<int:user_id>', views.view_profile, name='profiles_detail'),
    
]