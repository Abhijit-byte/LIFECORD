# In your app's urls.py
from django.urls import path
from . import views
# 🌟 ADD THIS IMPORT LINE 🌟
from django.contrib.auth import views as auth_views
urlpatterns = [
    # --- Frontend/Page Views ---
    path('', views.send_otp_page, name='send_otp_page'),
    path('verify_otp_page/', views.verify_otp_page, name='verify_otp_page'),
    path('dashboard/', views.dashboard, name='dashboard'), # Patient Dashboard
    path('hospital-dashboard/', views.hospital_dashboard, name='hospital_dashboard'), # Staff Dashboard4
    path('hospital-dashboard/<int:hospital_id>/', 
         views.hospital_dashboard, 
         name='hospital_dashboard'),
         
    # --- Hospital Dashboard API Endpoint (Filtered by ID) ---
    path('api/hospitaldashboard/<int:hospital_id>/', 
         views.get_dashboard_data, 
         name='get_filtered_dashboard_data'),
    path('check_patient_exists/', views.check_patient_exists, name='check_patient_exists'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    
    # --- Hospital Dashboard API Endpoint (Filtered by ID) ---
    # The view 'get_dashboard_data' requires the hospital_id parameter, 
    # so we map the path that provides it.
    path('api/hospitaldashboard/<int:hospital_id>/', views.get_dashboard_data, name='get_filtered_dashboard_data'),
    
    path('staff-login/', auth_views.LoginView.as_view(template_name='accounts/staff_login.html'), name='staff_login'),
    path('staff-logout/', auth_views.LogoutView.as_view(), name='staff_logout'),
    
    # REMOVED: path('api/dashboard/', views.get_dashboard_data, name='get_dashboard_data'),
    # This was removed because it conflicts with the new path's name, and the view function 
    # 'get_dashboard_data(request, hospital_id)' expects the ID.
]