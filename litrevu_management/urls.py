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

from django.urls import path
import litrevu_management.views as views

app_name = "litrevu"

urlpatterns = [
    path('', views.home, name='home'),
    path('review/ticket/create/', views.create_ticket, name='create_ticket'),
    path('review/create/', views.create_review, name='create_review'),  # créer une critique
    path('posts/', views.posts, name='posts')
]
