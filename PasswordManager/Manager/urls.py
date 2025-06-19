from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('add/', views.add_password, name='add_password'),
    path("logout/", views.logout_view, name="logout"),
    path('delete/', views.delete_password, name='delete_password'),
    path('update/<int:id>/', views.update_password, name='update_password'),
]