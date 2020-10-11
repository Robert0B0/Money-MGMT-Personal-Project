from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class moneyUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    worth = models.DecimalField(null=False, max_digits=7, decimal_places=2)
    email = models.EmailField(max_length=200, null=True)
    profile_pic = models.ImageField(default="default_money_user.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

class moneyGoals(models.Model):
    CATEGORY = (
                ('Small Goal', 'Small Goal'),
                ('Liability Goal', 'Liability Goal'),
                ('Life Goal', 'Life Goal'),
                ('Investment Goal', 'Investment Goal'),
                )

    user = models.ForeignKey(moneyUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False)
    category = models.CharField(max_length=200, null=False, choices=CATEGORY, default='Small Goal')
    amount = models.DecimalField(null=False, max_digits=7, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    due_date = models.DateTimeField(auto_now_add=False, null=True)
    calculated_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.naming)

class moneyActivity(models.Model):
    CATEGORY = (
                ('Outcome', (
                            ('expenses', 'Expenses'),
                            ('upkeep', 'Upkeep'),
                            ('unforeseen', 'Unforeseen'),
                            )
                ),
                ('Income', (
                            ('monthly income', 'Monthly Income'),
                            ('dividents', 'Dividents'),
                            ('other', 'Other'),
                            )
                ),
            )
    
    user = models.ForeignKey(moneyUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, blank=True, default="Expenses")
    category = models.CharField(max_length=200, null=False, choices=CATEGORY, default='Outcome')
    amount = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '€' + str(self.amount)







    