"""
URL configuration for ScrumMasters361 project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
import TAScheduler.views as views

urlpatterns = [
    path('', views.Login.as_view()),
    path('profile/', views.OtherAccount.as_view()),
    path('admin/', admin.site.urls),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('home/', views.Home.as_view()),
    path('create_user/', views.CreateUser.as_view()),
    path('create_course/', views.CreateCourse.as_view()),
    path('create_section/', views.CreateSection.as_view()),
    path('accounts/', views.Accounts.as_view()),
    path('sections/', views.Sections.as_view()),
    path('edit_user/', views.EditUser.as_view()),
    path('edit_section/', views.EditSection.as_view()),
    path('edit_section/add_ta/', views.AddSectionTA.as_view()),
    path('edit_section/remove_ta/', views.RemoveSectionTA.as_view()),
    path('delete_user/', views.DeleteUser.as_view()),
    path('modify_account/', views.ModifyAccount.as_view()),
    path('courses/', views.Courses.as_view()),
    path('edit_course/', views.EditCourse.as_view())
]
