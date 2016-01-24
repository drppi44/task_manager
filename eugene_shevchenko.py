class Task(object):
    def __init__(self, name, complexity):
        self.name = name
        self.complexity = complexity
        self.bound = False

    def __repr__(self):
        return '%s  %dcp' % (self.name, self.complexity)


class Employee(object):
    def __init__(self, name, cp_per_time):
        self.name = name
        self.cp_per_time = cp_per_time
        self.tasks = []

    def __repr__(self):
        return '%s  load=%f' % (self.name, self.load)

    @property
    def total_cp(self):
        return sum(task.complexity for task in self.tasks)

    @property
    def load(self):
        return self.total_cp / float(self.cp_per_time)


class TaskManager(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(TaskManager, cls).__new__(cls, *args,
                                                            **kwargs)
        return cls._instance

    def __init__(self, tasks=list(), employees=list()):
        self.tasks = tasks
        self.employees = employees

    def create_empoyee(self, *args, **kwargs):
        self.employees.append(Employee(*args, **kwargs))

    def create_task(self, *args, **kwargs):
        self.tasks.append(Task(*args, **kwargs))

    def manage(self):
        for task in self.tasks:
            if not task.bound:
                less_loaded_employee = min(self.employees,
                                           key=lambda emp: emp.load)
                less_loaded_employee.tasks.append(task)
                task.bound = True


