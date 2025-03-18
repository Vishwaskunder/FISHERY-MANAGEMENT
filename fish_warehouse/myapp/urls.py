"""fish_warehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from myapp import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("admin__user/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
    path("admin_user/add_users/", views.add_users_view, name="add_users"),

    #path('add_f/', views.add_f_view, name='add_f'),
    path("add-fish/", views.add_fish_view, name="add_fish"),
    path("delete-fish/<str:fish_name>/", views.delete_fish_view, name="delete_fish"),
    path("admin_user/all_fishes",views.fishes,name="fishes"),
    path("admin_user/update_fish/<str:fish_name>",views.edit_fishes,name="edit_fish"),
    
    path("view_users/",views.view_users,name="view_users"),
    
    path('sell-fish/<int:fish_id>',views.sell_fish, name='sell_fish'),
    
    path("all_fishes",views.all_fishes,name="all_fishes"),
 
    path("order/<int:fish_id>",views.order,name="order"),
   
    path("orderdetails/",views.orderdetails,name="orderdetails"),
    
    
    path("home_warehouse/",views.home_warehouse,name="home_warehouse"),
    
    # path("sell_fish/<str:fish_name>",views.sell_fish,name="sell_fish"),
    # path('sell-fish/<int:fish_id>/',views.sell_fish, name='sell_fish'),

    path("view_profile/<int:id>/",views.view_profile,name="view_profile"),
    path("view_profile_fish/<str:fish_name>/",views.view_profile_fish,name="view_profile_fish"),

    path("admin_dashboard/",views.admin_dashboard_2,name="admin_dashboard_2"),
]


