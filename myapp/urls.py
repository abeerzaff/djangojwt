
from django.urls import path
from .views import RegisterView, LoginView  , ProfileView


print("✅ myapp.urls loaded")
urlpatterns = [
   path('register/',RegisterView.as_view(),name="auth_register"),
   path('login/',LoginView.as_view(),name="auth_login"),
    path('profile/', ProfileView.as_view(), name='user-profile'),
 
   
]
