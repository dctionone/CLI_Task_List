# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 19:09:24 2025

@author: DC

##NOTES##

DEVELOP CLI-USER EXPERIENCE  
    -clean up, it's ugly af
    
MAJOR ISSUES:

    -need to learn how to import json dict and convert to Task class so i can update existing files
                                  

"""

from datetime import datetime
import json
from json import JSONEncoder
from dataclasses import dataclass


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
    
    def set_name(self, name):
        self.name = name
        
        # self.container['Name'] = name
    
    def set_status(self, status):
        """Status should be an int (1-3):
            1. TODO
            2. COMPLETED
            3. IN PROGRESS"""
            
        assert type(status) == int
        status_list = ['TODO', 'COMPLETED', 'IN PROGRESS']
        try: 
            self.status = status_list[status-1]

        except:
            raise ValueError('Status must be an int 1-3')
            
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.status
    
    def json_rep(self):
        
        container = {}
        container['id'] = self.id
        container['Name'] = self.name
        container['Status'] = self.status
        container['Birth Time'] = self.birth_time
        container['Updated at'] = self.time
        
        
        return container
        
    def task_decoder(dict_):
        return Task(**dict_)
    
    def __str__(self):
        return str(self.id) + ' ' + self.name + ' ' + self.status + ' created at ' + \
               self.birth_time + ' updated at ' + self.time##change this later
    
        
    
    
class Task_List(Task):
    def __init__(self):
        self.tasks = []
        
    
    def add_task(self, task):
        '''assumes Task is a Task object'''
        if task.get_id() not in range(len(self.tasks)):
            self.tasks.append(task)
            return f'{task.get_name()} added successfully'
        else:
            return f'{task.get_name()} is already in the list!'
    
    def remove_task(self, list_num):
        '''list_num is the # of the task on the list'''
        
        a = list_num - 1
        
        if a in range(len(self.tasks)):
            self.tasks.pop(a)   
        else:
            return 'Task was not in the list!'
        
        return 'Task removed successfully!'
    
    def update_status(self, list_num, status_num):
        for task in self.tasks:
            if task.get_id() == list_num:
                task.set_status(status_num)
        
        
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

def task_list_decoder(dict_):
    return Task_List(**dict_)    
    
def file_save(filename):
    with open(filename, "w") as outfile:
        outfile.write(filename)
            
def file_open(filename):
    with open(filename, "r") as openfile:
        json.load(openfile, object_hook=task_list_decoder)
        
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
    
    prompt = input('What would you like to do? \n1. Add a task \n2. Update a task \n\
3. Delete a task \n4. List all completed tasks\n\
5. List all uncompleted tasks \n6. List all tasks in progress \n7. Close the program\n')
    
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
            ##print all tasks with status 2
            task_list.print_status('IN PROGRESS')
            
            return task_list_options(file_name, task_list)
                    
        if prompt==5:
            ##print all tasks with status 1
            task_list.print_status('TODO')
            return task_list_options(file_name, task_list)
            
        if prompt==6:
            # print all tasks with status 3
            task_list.print_status('COMPLETED')
            return task_list_options(file_name, task_list)
            
        if prompt==7:
            return False
        else:
            return task_list_options(file_name, task_list)
        
    
def opentl(start=True):
    '''function to start CLI'''
    
    while start:
        file_name = input('What is the title of your list? ')
        try: 
            task_list = file_open(file_name)
        except:
            file_save(file_name)
            task_list = Task_List()
        
        
        start = task_list_options(file_name, task_list)      ##recursive function to continue prompting until user is done
        
        
        
        
        
        
        
            
            
        
  
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



    
