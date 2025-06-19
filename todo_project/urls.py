from django.contrib import admin
from django.urls import path, include
from todo.views import register_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register_view, name='register'),
    path('', include('todo.urls')),  # your app
    path('accounts/', include('django.contrib.auth.urls')),  # ← this line
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]