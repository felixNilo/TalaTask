from django.db import models
from multiselectfield import MultiSelectField

DAY_CHOICES = [
    ('MO', 'Monday'),
    ('TU', 'Tuesday'),
    ('WE', 'Wednesday'),
    ('TH', 'Thursday'),
    ('FR', 'Friday'),
]

class Skill(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    skills = models.ManyToManyField('Skill')   
    #this is average hours per day. For example, if the Employee has 2 days available, and 10 hours, it means that
    #the user has 20 available hours.
    #so, if the user takes a 10 hours task, the field available_hours_per_day take the value of 5.    
    available_hours_per_day = models.DecimalField(max_digits=5, decimal_places=2)
    available_days = MultiSelectField(choices=DAY_CHOICES)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.IntegerField() #total task duration.
    required_skills = models.ManyToManyField('Skill')
    assigned_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    