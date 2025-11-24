from django.urls import path
from . import views

urlpatterns = [
    path("send_otp/", views.send_otp, name="send_otp"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("", views.send_otp_page, name="send_otp_page"),
    path("verify_otp_page/", views.verify_otp_page, name="verify_otp_page"),
    path("dashboard/", views.dashboard, name="dashboard"),

]
