from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    #path('login/', views.loginPage, name="login"),
    #path('register/', views.registerPage, name="register"),
    path('setting/', views.settingsPage, name="settings"),

    path('', views.homePage, name="home"),
    
    path('activities/', views.actPage, name="act_page"),
    path('activity_form/', views.createAct, name="act_form"),
    path('update_activity/<str:pk>/', views.updateAct, name="update_act"),
    path('delete_activity/<str:pk>/', views.deleteAct, name="delete_act"),

    path('goals/', views.goalsPage, name="goals_page"),
    path('goal_form/', views.createGoal, name="goal_form"),
    path('update_goal/<str:pk>/', views.updateGoal, name="update_goal"),
    path('delete_goal/<str:pk>/', views.deleteGoal, name="delete_goal"),

    path('graph/', views.graphPage, name="graphs"),


]
