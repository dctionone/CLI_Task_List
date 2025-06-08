# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 19:09:24 2025

@author: DC

##NOTES##

DEVELOP CLI-USER EXPERIENCE  
    -clean up, it's ugly af
                                  
CAN ADD FUNCTIONALITY TO OPEN ANOTHER LIST
CAN STILL ADD SAME TASK MULTIPLE TIMES
COULD USE MORE FAILSAFES WITHIN OPTION MENUS FOR INCORRECT INPUTS
"""

from datetime import datetime
import json
from json import JSONEncoder

class Task(object):
    _id_counter = 0
    
    def __init__(self, name):
        Task._id_counter += 1
        self.id = Task._id_counter
        self.name = name
        self.status = ''
        self.birth_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
        
    def get_name(self):
        return self.name
    
    def get_status(self):
        return self.status
    
    def get_id(self):
        return self.id
    
    def set_id(self, number):
        self.id = number
    
    def set_name(self, name):
        self.name = name
        
    def set_birth_time(self, time):
        self.birth_time = time
    
    def set_status(self, status):
        """Status should be an int (1-3):
            1. TODO
            2. COMPLETED
            3. IN PROGRESS"""            
        status_list = ['TODO', 'COMPLETED', 'IN PROGRESS']
        try: 
            self.status = status_list[status-1]
        except:
            self.status = status        
        return self.status
    
    def last_updated_time(self, time):
        self.time = time
    
    def update_time(self):
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def json_rep(self):
        '''function that converts task object into json readable dict '''
        container = {}
        container['id'] = self.id
        container['Name'] = self.name
        container['Status'] = self.status
        container['Birth Time'] = self.birth_time
        container['Updated at'] = self.time
        return container
   
    def __str__(self):
        return str(self.id) + ' ' + self.name + ' ' + self.status + ' created at ' + \
               self.birth_time + ' updated at ' + self.time  
    
class Task_List(Task):
    def __init__(self):
        self.tasks = []        
    
    def add_task(self, task):
        '''assumes task is a Task object'''
        if task.get_name() not in self.tasks: ##currently unable to check if names are alr in task_list
            self.tasks.append(task)
            return f'{task.get_name()} added successfully'
        else:
            return f'{task.get_name()} is already in the list!'
    
    def remove_task(self, task_id):
        '''task_id is the # of the task on the list'''       
        for task in self.tasks:
            if task.get_id() == task_id:
                index = self.tasks.index(task)
                self.tasks.pop(index)  
    
    def update_status(self, task_id, status_num):
        """assumes task_id and status_num are ints 
            Status should be an int (1-3):
            1. TODO
            2. COMPLETED
            3. IN PROGRESS"""
        for task in self.tasks:
            if task.get_id() == task_id:
                task.set_status(status_num)
                task.update_time()
            else:
                print('No Task Found')
        
        
    def print_status(self, status):
        for task in self.tasks:
            if task.get_status() == status:
                print(task)
    
    def json_rep(self):
        task_dict = {}
        for i in range(len(self.tasks)):
            task_dict[i] = self.tasks[i]
        return task_dict
        
    def __str__(self):
        a= ''
        for i in self.tasks:
            a+= f'{i} \n'
        return a
   
    
def file_save(filename):
    with open(filename, "w") as outfile:
        data = outfile.write(filename)
        return data
            
def file_open(filename):
    with open(filename, "r") as openfile:
        task_list = json.load(openfile)
        return task_list
        
def save(tasklist, filename):
    with open(filename, "w") as file:
        try:
            json.dump(tasklist, file, indent=4, cls=encoder)
            
        except:
            json.dumps(tasklist, indent=4, cls=encoder)
            
class encoder(JSONEncoder):
    """class to encode Task/Task_List objects to be json readable"""
    def default(self, o):
        return o.__dict__
        
        
def task_list_options(file_name, task_list):
    """function that stores file_name(str) and task_list(Task_List object) and prompts CLI for user"""
    
    prompt = input('What would you like to do? \n1. Add a task \n2. Update a task \n\
3. Delete a task \n4. List all tasks \n5. List all TODO \n6. List all COMPLETED tasks \n7. List all tasks IN PROGRESS \n8. Close the program\n')
    
    if len(prompt) > 1 or prompt in 'abcdefghijklmnopqrstuvwxyz':
        return task_list_options(file_name, task_list)      
    
    else:
        prompt = int(prompt)   
        if prompt == 1:
        ##prompt through function to add task, use Task_List.add_task(prompt)
            task = input('What task would you like to add? \n') ##add this to the add task function
            task = Task(task)  ##instantiating first task
            status = input('Enter a number to indicate the status of your task: \nStatus should be an int (1-3): \n1. TODO\n2. COMPLETED \n3. IN PROGRESS\n')
            task.set_status(int(status)) ##convert to int for function readability
            task.update_time()
            task_list.add_task(task)
            print(task_list)
            save(task_list.json_rep(), file_name)    ##save to json    
            return task_list_options(file_name, task_list)
            ##print all tasks then prompt for which task_id to update
            ##receive status input, use task_id find task in task_list and then set_status
        
        if prompt == 2:
            print(task_list)
            task_id = input('\nWhat task would you like to update? (Enter the task id #)\n') ##add this to the add task function
            task_id = int(task_id) 
            status = input('Enter a number to indicate the status of your task: \nStatus should be an int (1-3): \n1. TODO\n2. COMPLETED \n3. IN PROGRESS\n')  ##MAYBE WRITE FUNCTION TO DO THIS TO AVOID DOUBLE
            status = int(status)
            ##need to find task in task list then set_status
            task_list.update_status(task_id, status)
            print(task_list)        
            save(task_list.json_rep(), file_name)
            return task_list_options(file_name, task_list)

        if prompt==3:
            ##print all tasks then prompt for which task_id to remove
            ##receive status_input, use task_id find task in task_list and then set_status
            print(task_list)
            delete = input('\nWhat task do you want to remove? (Enter the task id #)\n')
            delete = int(delete)
            task_list.remove_task(delete)
            print(task_list)
            save(task_list.json_rep(), file_name)
            return task_list_options(file_name, task_list)
        
        if prompt==4:
            print(task_list)
            return task_list_options(file_name, task_list)
            
        if prompt==5:
            ##print all tasks with status 1
            task_list.print_status('TODO') 
            return task_list_options(file_name, task_list)
                    
        if prompt==6:
            ##print all tasks with status 2
            task_list.print_status('COMPLETED')
            return task_list_options(file_name, task_list)
            
        if prompt==7:
            # print all tasks with status 3
            task_list.print_status('IN PROGRESS')
            return task_list_options(file_name, task_list)
            
        if prompt==8:          
            return False
        else:
            return task_list_options(file_name, task_list)


def convertJSON_to_Task(json):
    start = []
    for values in json.values():
        start.append(values)
    task_list = Task_List()  
    for tasks in start: ##list of dicts
        a= Task(tasks['name'])
        a.set_id(tasks['id'])
        a.set_status(tasks['status'])
        a.set_birth_time(tasks['birth_time'])  ###PROBLEM - wILL FORCE UPDATE (UPDATE TIME) EVERY TIME YOU RE-OPEN THE PROGRAM
        a.last_updated_time(tasks['time'])
        task_list.add_task(a)
        
    return task_list
    
def opentl(start=True):
    '''function to start CLI'''
    
    while start:
        file_name = input('What is the title of your list? ')
        try: 
            task_list = file_open(file_name) 
            task_list = convertJSON_to_Task(task_list)
        except: 
            file_save(file_name)
            task_list = Task_List()
        start = task_list_options(file_name, task_list)      
                
   
opentl()    
    
        
##TEST CODE##        
# a, b, c = Task('code'), Task('Brush Teeth'), Task('Do dishes')
# # a.set_status(3)
# # b.set_status(2)
# # c.set_status(1)
# d = Task_List()
# d.add_task(a)
# d.add_task(b)
# d.add_task(c)
# print(d)
# # d.remove_task(2)
# # print(d)
# e = Task('buy groceries')
# e.set_status(2)
# d.add_task(e)
# b.set_name('booyaka')
# b.set_status(3)
# print(d)



    
