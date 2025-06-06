# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 19:09:24 2025

@author: DC

                                             

"""

from datetime import datetime
import json


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
    
    def __str__(self):
        return str(self.id) + ' ' + self.name + ' ' + self.status + ' created at ' + \
               str(self.birth_time) + ' updated at ' + str(self.time)
    
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
        
    def update_task(self, list_num, status):
        '''list_num is the # of the task on the list and status an int (1-3)'''
          
        for i in self.tasks:
            if list_num == i.get_id():   
                return i.set_status(status)
                
            else:
                return f'({i.get_name()} was not in the list!)'
        
    def __str__(self):
        a= ''
        for i in self.tasks:
            a+= f'{i} \n'
        return a
    
    
    # def file_save(self):
    #     json_array = json.dumps(self.tasks)
    #     with open("task_list.json", "w") as outfile:
    #         outfile.write(json_array)
            
    # def file_open(self):
    #     with open("task_list.json", "r") as openfile:
    #         json.load(openfile)
        
        
a, b, c = Task('code'), Task('Brush Teeth'), Task('Do dishes')
a.set_status(3)
b.set_status(2)
c.set_status(1)
d = Task_List()
d.add_task(a)
d.add_task(b)
d.add_task(c)
# print(d)

# d.remove_task(2)
# print(d)
e = Task('buy groceries')
e.set_status(2)
d.add_task(e)
d.update_task(1, 3)

print(d)

    
