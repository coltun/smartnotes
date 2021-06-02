from django.urls import path
from account import views
from account.views import CustomLoginView, CustomLogoutView

app_name = 'account'

urlpatterns = [
	path('', views.homepage, name='homepage'),
	path('notes/', views.display_notes, name='notes'),
	path('user/settings/', views.user_settings, name='user_settings'),
	path('user/instructions', views.user_instructions, name='user_instructions'),
	path('register/', views.register, name='register'),
	path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
	
	
	
]