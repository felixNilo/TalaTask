from collections import defaultdict
from .models import Employee, Task

def assign_tasks():
    # get all unassigned task and all employees
    tasks = Task.objects.filter(assigned_employee__isnull=True)
    employees = Employee.objects.all()

    assignments = defaultdict(lambda: {
        'total_hours_assigned': 0,
        'remaining_hours': 0,
        'tasks': [],
        'skills_used': set()
    })

    for task in tasks:
        #get the task day code
        task_day_code = task.date.strftime('%a')[:2].upper()
        required_skills = set(task.required_skills.all())  #performance improvement

        for employee in employees:
            employee_skills = set(employee.skills.all())  #performance improvement
            is_available_on_task_date = task_day_code in employee.available_days

            #check if the employee has the required skills
            has_required_skills = required_skills.issubset(employee_skills)

            #clculate the total available hours for the employee
            total_available_hours = employee.available_hours_per_day * len(employee.available_days)

            #check if the employee has sufficient hours available
            has_sufficient_hours = total_available_hours >= task.duration

            if has_required_skills and is_available_on_task_date and has_sufficient_hours:
                #assign the task to the employee
                task.assigned_employee = employee
                task.save()

                #reduce the employee available hours
                total_available_hours -= task.duration
                employee.available_hours_per_day = total_available_hours / len(employee.available_days)
                employee.save()
                
                #update the assignments dictionary
                assignments[employee.name]['total_hours_assigned'] += task.duration
                assignments[employee.name]['remaining_hours'] = total_available_hours
                assignments[employee.name]['tasks'].append({
                    'task_title': task.title,
                    'duration': task.duration,
                    'skills_used': sorted([skill.name for skill in required_skills])
                })

                break  #task assigned, move to the next task
    
    return assignments
