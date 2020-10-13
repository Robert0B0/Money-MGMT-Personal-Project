from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum

from .models import *
from .forms import *


#==================| global variables |==================================


#records = moneyRecord.objects.all()
#goals = moneyGoals.objects.all()
#total_records = records.count()
#total_goals = goals.count()
#
#user_name = moneyUser.objects.get(pk=1).name
#wallet = moneyUser.objects.get(pk=1).worth
#
#
#total_out = moneyRecord.objects.filter(category='Outcome').aggregate(Sum('amount'))
#total_amount_out = total_out['amount__sum']
#    
#balance = wallet

#=================| ACCOUNT SETTINGS |=========================================
def settingsPage(request):
    context = {}

    return render(request, 'MGMT/settings.html', context)

#=================| Status PAGE |=========================================

def statusPage(request):

    context = {'records': records, 'goals': goals, 
    'total_records': total_records, 'total_goals': total_goals,
    'user_name': user_name, 'balance': balance}

    return render(request, 'status.html', context)

#=================| HOME PAGE |=========================================

def homePage(request):
    records = moneyRecord.objects.all()
    goals = moneyGoals.objects.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = moneyUser.objects.get(pk=1).name
    wallet = moneyUser.objects.get(pk=1).worth

    total_out = moneyRecord.objects.filter(category='Outcome').aggregate(Sum('amount'))
    total_amount_out = total_out['amount__sum']

    balance = wallet

    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/home.html', context)

#=================| MONETARY Record |=========================================

def recordPage(request):
    records = moneyRecord.objects.all()
    goals = moneyGoals.objects.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = moneyUser.objects.get(pk=1).name
    wallet = moneyUser.objects.get(pk=1).worth

    total_out = moneyRecord.objects.filter(category='Outcome').aggregate(Sum('amount'))
    total_amount_out = total_out['amount__sum']

    balance = wallet

    total_expenses = moneyRecord.objects.filter(category='expenses').aggregate(Sum('amount'))['amount__sum']
    total_upkeep = moneyRecord.objects.filter(category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_unforeseen = moneyRecord.objects.filter(category='unforeseen').aggregate(Sum('amount'))['amount__sum']

    total_income = moneyRecord.objects.filter(category='monthly income').aggregate(Sum('amount'))['amount__sum']
    total_dividents = moneyRecord.objects.filter(category='dividents').aggregate(Sum('amount'))['amount__sum']
    total_in_other = moneyRecord.objects.filter(category='other').aggregate(Sum('amount'))['amount__sum']

    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance, 
        'total_expenses' : total_expenses, 'total_upkeep': total_upkeep, 'total_unforeseen': total_unforeseen,
        'total_income': total_income, 'total_dividents': total_dividents, 'total_in_other': total_in_other}

    return render(request, 'MGMT/record_page.html', context)

def createRecord(request, pk):
    user = moneyUser.objects.get(id=pk)
    form = RecordForm(initial={'user': user})
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid:
            form.save()

            return redirect('/')

    context = {'form': form}

    return render(request, 'MGMT/record_form.html', context)

def updateRecord(request, pk):
    act = moneyRecord.objects.get(id=pk)
    form = RecordForm(instance=act)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=act)
        if form.is_valid:
            form.save()
            return redirect('/records/')

    context = {'form': form}

    return render(request, 'MGMT/record_form.html', context) 

def deleteRecord(request, pk):
    record = moneyRecord.objects.get(id=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('/records/') 
    context ={'record': record}

    return render(request, 'MGMT/record_delete.html', context)



#=================| GOALS |=========================================

def goalsPage(request):
    records = moneyRecord.objects.all()
    goals = moneyGoals.objects.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = moneyUser.objects.get(pk=1).name
    wallet = moneyUser.objects.get(pk=1).worth

    total_out = moneyRecord.objects.filter(category='Outcome').aggregate(Sum('amount'))
    total_amount_out = total_out['amount__sum']

    balance = wallet

    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
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

#=================| SAVINGS |=========================================


def savingsPage(request):
    context = {}

    return render(request, 'MGMT/savings_page.html', context)

def createSaving(request):
    context = {}

    return render(request, 'MGMT/savings_page.html', context)


#=================| GRAPHS |=========================================

def graphPage(request):
    records = moneyRecord.objects.all()
    goals = moneyGoals.objects.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = moneyUser.objects.get(pk=1).name
    wallet = moneyUser.objects.get(pk=1).worth

    total_out = moneyRecord.objects.filter(category='Outcome').aggregate(Sum('amount'))
    total_amount_out = total_out['amount__sum']

    balance = wallet
    
    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/graph.html', context)

#=================| |=========================================