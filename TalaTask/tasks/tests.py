from django.test import TestCase
from tasks.models import Employee, Skill, Task
from tasks.services import calculate_available_days, calculate_total_available_hours, assign_tasks
from datetime import datetime, timedelta

class ServicesTestCase(TestCase):
    def setUp(self):
        #create base skills
        self.skill1 = Skill.objects.create(name="tech_lvl_1")
        self.skill2 = Skill.objects.create(name="proc_lvl_1")
        self.skill3 = Skill.objects.create(name="com_lvl_1")
        self.skill4 = Skill.objects.create(name="lead_lvl_1")

        #create employee
        self.employee1 = Employee.objects.create(
            name="John Doe",
            available_hours_per_day=8,
            available_days=['MO', 'TU', 'WE'],
        )
        self.employee1.skills.add(self.skill1, self.skill2, self.skill3, self.skill4)
        
        #create task
        self.task1 = Task.objects.create(
            date=datetime(2024, 9, 11).date(),  #random known day
            duration=4,
        )
        self.task1.required_skills.add(self.skill1, self.skill2, self.skill3, self.skill4)

    def test_calculate_available_days(self):
        start_date = datetime(2024, 9, 6).date()  #random known day
        end_date = start_date + timedelta(days=7)
        available_days = calculate_available_days(self.employee1, start_date, end_date)
        self.assertEqual(available_days, 3) #Mo, Tu, We

    def test_calculate_total_available_hours(self):
        start_date = datetime(2024, 9, 6).date() #random known day
        end_date = start_date + timedelta(days=7)
        total_hours = calculate_total_available_hours(self.employee1, start_date, end_date)
        self.assertEqual(total_hours, 24)  #3 days, 8 hour per day.

    def test_assign_tasks(self):
        assignments = assign_tasks()
        self.task1.refresh_from_db()
        self.assertIsNotNone(self.task1.assigned_employee)
        self.assertEqual(assignments[self.employee1.name]['total_hours_assigned'], 4)
