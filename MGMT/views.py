from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum

from .models import *
from .forms import *


#==================| global variables |==================================


activities = moneyActivity.objects.all()
goals = moneyGoals.objects.all()
user_name = moneyUser.objects.get(pk=1).name
total_activities = activities.count()
total_goals = goals.count()

wallet = moneyUser.objects.get(pk=1).worth
user_name = moneyUser.objects.get(pk=1).name
total_activities = activities.count()
total_goals = goals.count()

total_out = moneyActivity.objects.aggregate(Sum('amount'))
total_amount_out = total_out['amount__sum']
    
balance = wallet - total_amount_out

#=================| ACCOUNT SETTINGS |=========================================
def settingsPage(request):
    context = {}

    return render(request, 'MGMT/settings.html', context)

#=================| Status PAGE |=========================================

def statusPage(request):

    context = {'activities': activities, 'goals': goals, 
    'total_activities': total_activities, 'total_goals': total_goals,
    'user_name': user_name, 'balance': balance}

    return render(request, 'status.html', context)

#=================| HOME PAGE |=========================================

def homePage(request):
    context = {'activities': activities, 'goals': goals, 
    'total_activities': total_activities, 'total_goals': total_goals,
    'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/home.html', context)

#=================| MONETARY ACTIVITY |=========================================

def actPage(request):
    total_val = moneyActivity.objects.aggregate(Sum('amount'))
    total_amount = total_val['amount__sum']

    context = {'activities': activities, 'goals': goals, 
    'total_activities': total_activities, 'total_goals': total_goals,
    'user_name': user_name, 'wallet': wallet, 'total_amount' : total_amount}

    return render(request, 'MGMT/act_page.html', context)

def createAct(request):
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid:
            form.save()

            return redirect('/')

    context = {'form': form}

    return render(request, 'MGMT/act_form.html', context)

def updateAct(request, pk):
    act = moneyActivity.objects.get(id=pk)
    form = ActivityForm(instance=act)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=act)
        if form.is_valid:
            form.save()
            return redirect('/activities/')

    context = {'form': form}

    return render(request, 'MGMT/act_form.html', context) 

def deleteAct(request, pk):
    activity = moneyActivity.objects.get(id=pk)
    if request.method == 'POST':
        activity.delete()
        return redirect('/activities/') 
    context ={'activity': activity}

    return render(request, 'MGMT/act_delete.html', context)



#=================| GOALS |=========================================

def goalsPage(request):
    context = {'activities': activities, 'goals': goals, 
    'total_activities': total_activities, 'total_goals': total_goals,
    'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/goals_page.html', context)

def createGoal(request):
    form = GoalForm()
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/goals/')

    context = {'form': form}

    return render(request, 'MGMT/goal_form.html', context)

def updateGoal(request, pk):
    goal = moneyGoals.objects.get(id=pk)
    form = GoalForm(instance=goal)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid:
            form.save()
            return redirect('/goals/')

    context = {'form': form}

    return render(request, 'MGMT/goal_form.html', context)

def deleteGoal(request, pk):
    goal = moneyGoals.objects.get(id=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('/goals/')
    
    context = {'goal': goal}

    return render(request, 'MGMT/goal_delete.html', context)


#=================| GRAPHS |=========================================

def graphPage(request):
    context = {'activities': activities, 'goals': goals, 
    'total_activities': total_activities, 'total_goals': total_goals,
    'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/graph.html', context)

#=================| |=========================================