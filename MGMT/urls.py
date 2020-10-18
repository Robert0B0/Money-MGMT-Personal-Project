from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('login/', views.loginPage, name="login_page"),
    path('register/', views.registerPage, name="register_page"),
    path('logout/', views.logoutUser, name="logout"),
    path('setting/', views.settingsPage, name="user-settings"),

    path('', views.homePage, name="home"),
    
    path('records/', views.recordPage, name="record_page"),
    path('record_form/<str:pk>/', views.createRecord, name="record_form"),
    path('update_record/<str:pk>/', views.updateRecord, name="update_record"),
    path('delete_record/<str:pk>/', views.deleteRecord, name="delete_record"),

    path('goals/', views.goalsPage, name="goals_page"),
    path('goal_form/', views.createGoal, name="goal_form"),
    path('update_goal/<str:pk>/', views.updateGoal, name="update_goal"),
    path('delete_goal/<str:pk>/', views.deleteGoal, name="delete_goal"),

    path('savings/', views.savingsPage, name="savings_page"),
    path('saving_form/', views.createSaving, name="savings_form"),
    path('savings_update/<str:pk>/', views.updateSaving, name="update_savings"),
    path('savings_delete/<str:pk>/', views.deleteSaving, name="delete_savings"),

    path('graph/', views.graphPage, name="graphs"),


]
