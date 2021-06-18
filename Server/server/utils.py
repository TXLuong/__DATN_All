from entity.monitor import Monitor
from entity.employee import Employee
import json
class Utils : 
    def __init__(self):
        pass
    def convert_to_monitor(self, data):
        monitor_person = Monitor(data)
        monitor_person.password = None
        print("truoc khi dumps : ", monitor_person.__dict__)
        print(json.dumps(monitor_person.__dict__))
        return json.dumps(monitor_person.__dict__)
    def convert_to_employee(self, data):
        employee_person = Employee(data)
        print(json.dumps(employee_person))
        return json.dumps(employee_person)
