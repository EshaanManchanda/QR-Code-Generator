from django.urls import path
from django.contrib.auth import views as auth_views
from qr import views

urlpatterns = [
    path('', views.index, name='home'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # User profile and preferences
    path('profile/', views.profile, name='profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    
    # QR code management
    path('qr-history/', views.qr_history, name='qr_history'),
    path('qr-detail/<int:qr_id>/', views.qr_detail, name='qr_detail'),
    path('qr-delete/<int:qr_id>/', views.delete_qr, name='delete_qr'),
    
    # Download and analytics
    path('download-qr/', views.download_qr, name='download_qr'),
    path('track-download/', views.track_download, name='track_download'),
    path('track-share/', views.track_share, name='track_share'),
    
    # API endpoints
    path('api/generate-qr/', views.generate_qr_api, name='generate_qr_api'),
    path('api/qr-codes/', views.list_qr_api, name='list_qr_api'),
    path('api/docs/', views.api_docs, name='api_docs'),
    
    # Other pages
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]