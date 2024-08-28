from collections import defaultdict
from .models import Employee, Task
from datetime import datetime, timedelta

def calculate_available_days(employee, start_date, end_date):
    #here we get the number of available days of the employee from today to the date of the task
    available_days_count = 0
    current_date = start_date

    while current_date <= end_date:
        day_code = current_date.strftime('%a')[:2].upper()
        if day_code in employee.available_days:
            available_days_count += 1
        current_date += timedelta(days=1)

    return available_days_count

def calculate_total_available_hours(employee, start_date, end_date,):
    #here we get the total hour available for the employee from today to the date of the task
    available_days = calculate_available_days(employee, start_date, end_date)
    total_available_hours = available_days * employee.available_hours_per_day
    return total_available_hours

def assign_tasks():
    # get all unassigned task and all employees
    tasks = Task.objects.filter(assigned_employee__isnull=True)
    employees = Employee.objects.all()

    assignments = defaultdict(lambda: {
        'total_hours_assigned': 0,
        'tasks': [],
    })
    
    today = datetime.now().date()

    for task in tasks:
        task_due_date = task.date
        required_skills = set(task.required_skills.all())

        for employee in employees:
            #get the available hour of the employee from today to due date.
            total_available_hours = calculate_total_available_hours(employee, today, task_due_date)
            
            if total_available_hours >= task.duration:               
                #check if the employee has the required skills
                has_required_skills = required_skills.issubset(set(employee.skills.all()))

                if has_required_skills:
                    task.assigned_employee = employee
                    task.save()

                    #reduce the employee available hours
                    total_available_hours -= task.duration
                    
                    #update the assignments dictionary
                    assignments[employee.name]['total_hours_assigned'] += task.duration
                    assignments[employee.name]['tasks'].append({
                        'task_title': task.title,
                        'due date': task_due_date,
                        'duration': task.duration,
                        'skills_used': sorted([skill.name for skill in required_skills])
                    })

                    break  #task assigned, move to the next task
        
    return assignments
