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
    path('admin/', admin.site.urls),
    path('', litrevu_management.views.home, name='home'),

    path('login/', users.views.user_login, name='login'),
    path('signup/', users.views.signup, name='signup'),
    path('logout/', users.views.logout_user, name='logout'),

    path('following/', users.views.following, name='following'),
    path('following/unfollow/<int:user_to_unfollow_id>/', users.views.unfollow_user, name='unfollow'),
    path('following/unblock/<int:user_to_unblock_id>/', users.views.unblock_user, name='unblock'),

    # demander une critique (creation de ticket)
    path('review/ticket/create/', litrevu_management.views.create_ticket, name='create_ticket'),
    path('review/create/', litrevu_management.views.create_review, name='create_review'),  # créer une critique

    path('posts/', litrevu_management.views.posts, name='posts')
]
