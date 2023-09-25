"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView  # vue générique de connexion
from django.urls import path
import users.views
import litrevu_management.views
from users.forms import LoginForm

urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name="login.html",
             redirect_authenticated_user=True,
             authentication_form=LoginForm
         ),
         name='login'),
    path('signup/', users.views.signup, name='signup'),
    path('logout/', users.views.logout_user, name='logout'),
    path('', litrevu_management.views.home, name='home'),
    path('admin/', admin.site.urls),
]
