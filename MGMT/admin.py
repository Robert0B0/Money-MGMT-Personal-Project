from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(moneyUser)
admin.site.register(moneyGoals)
admin.site.register(moneyRecord)
admin.site.register(savingsJar)
admin.site.register(completedmoneyGoals)
admin.site.register(growthInvestment)


