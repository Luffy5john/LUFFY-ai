"""
JARVIS Task Automation - Intelligent Task Management and Reminders
"""

import datetime
import json
import os
import threading
import time
from collections import defaultdict

class TaskAutomation:
    def __init__(self, data_dir="jarvis_data"):
        self.data_dir = data_dir
        self.tasks = []
        self.reminders = []
        self.automation_rules = []
        self.active_timers = {}
        
        self.load_tasks()
        
    def load_tasks(self):
        """Load saved tasks and reminders"""
        try:
            tasks_file = os.path.join(self.data_dir, "tasks.json")
            if os.path.exists(tasks_file):
                with open(tasks_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.reminders = data.get('reminders', [])
                    self.automation_rules = data.get('automation_rules', [])
        except Exception as e:
            print(f"Error loading tasks: {e}")
    
    def save_tasks(self):
        """Save tasks and reminders"""
        try:
            tasks_file = os.path.join(self.data_dir, "tasks.json")
            data = {
                'tasks': self.tasks,
                'reminders': self.reminders,
                'automation_rules': self.automation_rules
            }
            with open(tasks_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, description, priority="medium", due_date=None):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'priority': priority,
            'status': 'pending',
            'created': datetime.datetime.now().isoformat(),
            'due_date': due_date,
            'completed': None
        }
        self.tasks.append(task)
        self.save_tasks()
        return f"Task added: {description}"
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed'] = datetime.datetime.now().isoformat()
                self.save_tasks()
                return f"Task {task_id} marked as completed, sir."
        return f"Task {task_id} not found, sir."
    
    def list_tasks(self, status="all"):
        """List tasks by status"""
        if status == "all":
            filtered_tasks = self.tasks
        else:
            filtered_tasks = [t for t in self.tasks if t['status'] == status]
        
        if not filtered_tasks:
            return "No tasks found, sir."
        
        task_list = []
        for task in filtered_tasks:
            priority_icon = "🔴" if task['priority'] == 'high' else "🟡" if task['priority'] == 'medium' else "🟢"
            status_icon = "✅" if task['status'] == 'completed' else "⏳"
            task_list.append(f"{status_icon} {priority_icon} {task['id']}: {task['description']}")
        
        return "Your tasks:\n" + "\n".join(task_list)
    
    def add_reminder(self, description, remind_time):
        """Add a reminder"""
        reminder = {
            'id': len(self.reminders) + 1,
            'description': description,
            'remind_time': remind_time,
            'created': datetime.datetime.now().isoformat(),
            'triggered': False
        }
        self.reminders.append(reminder)
        self.save_tasks()
        
        # Start reminder timer
        self.start_reminder_timer(reminder)
        return f"Reminder set for {remind_time}: {description}"
    
    def start_reminder_timer(self, reminder):
        """Start a timer for a reminder"""
        def reminder_worker():
            try:
                remind_datetime = datetime.datetime.fromisoformat(reminder['remind_time'])
                current_time = datetime.datetime.now()
                
                if remind_datetime > current_time:
                    sleep_seconds = (remind_datetime - current_time).total_seconds()
                    time.sleep(sleep_seconds)
                    
                    if not reminder['triggered']:
                        reminder['triggered'] = True
                        self.save_tasks()
                        # This would trigger a notification in the main system
                        print(f"REMINDER: {reminder['description']}")
                        
            except Exception as e:
                print(f"Reminder error: {e}")
        
        timer_thread = threading.Thread(target=reminder_worker, daemon=True)
        timer_thread.start()
        self.active_timers[reminder['id']] = timer_thread
    
    def add_automation_rule(self, trigger, action, description):
        """Add automation rule"""
        rule = {
            'id': len(self.automation_rules) + 1,
            'trigger': trigger,
            'action': action,
            'description': description,
            'created': datetime.datetime.now().isoformat(),
            'active': True
        }
        self.automation_rules.append(rule)
        self.save_tasks()
        return f"Automation rule added: {description}"
    
    def check_automation_triggers(self, context):
        """Check if any automation rules should trigger"""
        triggered_actions = []
        
        for rule in self.automation_rules:
            if not rule['active']:
                continue
                
            trigger = rule['trigger']
            
            # Time-based triggers
            if trigger['type'] == 'time':
                current_hour = datetime.datetime.now().hour
                if current_hour == trigger['hour']:
                    triggered_actions.append(rule['action'])
            
            # Context-based triggers
            elif trigger['type'] == 'context':
                if trigger['condition'] in str(context):
                    triggered_actions.append(rule['action'])
        
        return triggered_actions
    
    def get_task_summary(self):
        """Get summary of tasks"""
        pending_tasks = len([t for t in self.tasks if t['status'] == 'pending'])
        completed_tasks = len([t for t in self.tasks if t['status'] == 'completed'])
        active_reminders = len([r for r in self.reminders if not r['triggered']])
        
        return {
            'pending_tasks': pending_tasks,
            'completed_tasks': completed_tasks,
            'active_reminders': active_reminders,
            'automation_rules': len(self.automation_rules)
        }
    
    def get_overdue_tasks(self):
        """Get overdue tasks"""
        current_time = datetime.datetime.now()
        overdue = []
        
        for task in self.tasks:
            if task['status'] == 'pending' and task['due_date']:
                try:
                    due_date = datetime.datetime.fromisoformat(task['due_date'])
                    if due_date < current_time:
                        overdue.append(task)
                except:
                    continue
        
        return overdue
    
    def suggest_task_optimization(self):
        """Suggest task optimizations based on patterns"""
        suggestions = []
        
        # Check for overdue tasks
        overdue = self.get_overdue_tasks()
        if overdue:
            suggestions.append(f"You have {len(overdue)} overdue tasks that need attention, sir.")
        
        # Check task completion patterns
        completed_today = [t for t in self.tasks if t['completed'] and 
                          datetime.datetime.fromisoformat(t['completed']).date() == datetime.date.today()]
        
        if len(completed_today) > 3:
            suggestions.append("Excellent productivity today, sir. You've completed multiple tasks.")
        elif len(completed_today) == 0 and len(self.tasks) > 0:
            suggestions.append("Consider tackling some pending tasks today, sir.")
        
        return suggestions
