from datetime import timedelta
import factory
from tasks.models import Employee, Skill, Task
from faker import Faker

fake = Faker()

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    name = factory.Faker('name')
    available_hours_per_day = factory.Faker('random_int', min=1, max=8)  
    available_days = factory.LazyFunction(lambda: fake.random_elements(elements=('MO', 'TU', 'WE', 'TH', 'FR'), unique=True, length=3))

    @factory.post_generation
    def skills(self, create, extracted):
        if not create:
            return
        if extracted:
            for skill in extracted:
                self.skills.add(skill)
        else:
            dimensions = ['tech', 'com', 'lead', 'proc']
            for dimension in dimensions:
                #select a random level
                level = fake.random_int(min=1, max=3)
                for lvl in range(1, level + 1):
                    skill_name = f'{dimension}_lvl_{lvl}'
                    skill = Skill.objects.get(name=skill_name)
                    self.skills.add(skill)

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Faker('job')
    date = factory.LazyFunction(lambda: fake.date_between(start_date='today', end_date='+2d') + timedelta(days=fake.random_int(min=2, max=30)))
    duration = factory.Faker('random_int', min=1, max=40)  #from 1 hour task to 1 week task.

    @factory.post_generation
    def required_skills(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for skill in extracted:
                self.required_skills.add(skill)
        else:
            dimensions = ['tech', 'com', 'lead', 'proc']
            for dimension in dimensions:
                level = fake.random_int(min=1, max=3)
                skill_name = f'{dimension}_lvl_{level}'
                skill = Skill.objects.get(name=skill_name)
                self.required_skills.add(skill)
