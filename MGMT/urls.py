# from django.contrib import admin
from django.urls import path

from django.contrib.auth import views
from . import views

urlpatterns = [

    path('login/', views.loginPage, name="login_page"),
    path('register/', views.registerPage, name="register_page"),
    path('logout/', views.logoutUser, name="logout"),
    path('setting/', views.settingsPage, name="user-settings"),

    path('', views.homePage, name="home"),
    
    path('records/', views.recordPage, name="record_page"),
    path('create_record/', views.createRecord, name="create_record"),
    path('record_form/<str:pk>/', views.updateRecord, name="record_form"),
    path('delete_record/<str:pk>/', views.deleteRecord, name="delete_record"),

    path('goals/', views.goalsPage, name="goals_page"),
    path('create_goal/', views.createGoal, name="create_goal"),
    path('goal_form/<str:pk>/', views.updateGoal, name="goal_form"),
    path('goal_complete/<str:pk>/', views.completeGoal, name="complete_goal"),
    path('delete_goal/<str:pk>/', views.deleteGoal, name="delete_goal"),

    path('savings/', views.savingsPage, name="savings_page"),
    path('savings_create/', views.createSaving, name="create_savings"),
    path('saving_form/<str:pk>/', views.updateSaving, name="savings_form"),
    path('break_delete/<str:pk>/', views.breakSaving, name="break_savings"),
    path('savings_delete/<str:pk>/', views.deleteSaving, name="delete_savings"),

    path('graph/', views.graphPage, name="graphs"),

    path('about/', views.aboutPage, name="about"),

]