from django.contrib import admin
from django.urls import path, include
from todo.views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register_view, name='register'),
    path('', include('todo.urls')),  # your app
    path('accounts/', include('django.contrib.auth.urls')),  # ← this line
    
]
