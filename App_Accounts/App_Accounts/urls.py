from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from App_Accounts import views
app_name='App_Accounts'
urlpatterns = [
    path('signup',views.Signupview,name='signup'),
    path('login',views.Loginview,name='login'),
    path('HRlogin',views.HRLoginview,name='HRlogin'),
    path('hlogin',views.hLoginview,name='hlogin'),
    path('logout',views.Logoutview,name='logout'),
    path('dashboard',views.Dashboard,name='dashboard'),
    path('profile-update',views.Profileupdate,name='profileupdate'),
    path('password-change/',views.PasswordChange,name="passwordchange"),
    path('reward/',views.reward,name="reward"),
    path('updatePoints/',views.updatePoints,name="updatePoints"),
    # path('reward/pudatePonts/',views.pudatePonts,name="pudatePonts"),
    path('dashboard/save_Apportionment/',views.save_Apportionment,name="save_Apportionment"),
    path('Certificate/',views.Certificate,name="Certificate") 
]
