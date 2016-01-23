from unittest import TestCase
from eugene_shevchenko import Task, Employee, TaskManager
from random import randint


class TaskTest(TestCase):
    def test_task_contains_its_data(self):
        data = {'name': 'anytank', 'complexity': 2}
        task = Task(**data)

        self.assertEqual(task.name, data['name'])
        self.assertEqual(task.complexity, data['complexity'])
        self.assertFalse(task.bound)

    def test_task_could_be_bound(self):
        data = {'name': 'anytank', 'complexity': 2}
        task = Task(**data)
        task.bound = True

        self.assertTrue(task.bound)


class EmployeeTest(TestCase):
    def setUp(self):
        self.employee_data = {'name': 'anyemployee', 'cp_per_time': 2}

    def test_employee_contains_its_data(self):
        employee = Employee(**self.employee_data)

        self.assertEqual(employee.name, self.employee_data['name'])
        self.assertEqual(employee.cp_per_time,
                         self.employee_data['cp_per_time'])
        self.assertEqual(employee.tasks, [])

    def test_total_cp_with_empty_tasks(self):
        employee = Employee(**self.employee_data)

        self.assertEqual(employee.total_cp, 0)

    def test_total_cp_with_tasks(self):
        tasks = [Task(name='task_%d' % i, complexity=randint(1, 5)) for i in
                 range(1, 11)]

        employee = Employee(**self.employee_data)
        employee.tasks = tasks

        self.assertEqual(employee.total_cp,
                         sum(task.complexity for task in tasks))

    def test_load_with_empty_tasks(self):
        employee = Employee(**self.employee_data)

        self.assertEqual(employee.load, 0)

    def test_load_with_tasks(self):
        employee = Employee(**self.employee_data)
        employee.tasks = [Task(name='task_%d' % i, complexity=randint(1, 5))
                          for i in range(1, 11)]

        self.assertEqual(employee.load,
                         employee.total_cp / float(employee.cp_per_time))


class ManagerTest(TestCase):
    def setUp(self):
        self.max_complexity = 5

    def _create_tasks(self, count):
        manager = TaskManager()
        for i in range(count):
            manager.create_empoyee('employee_%d' % i,
                                   randint(1, self.max_complexity))

    def _create_employees(self, count):
        manager = TaskManager()
        for i in range(10):
            manager.create_empoyee('employee_%d' % i,
                                   randint(1, self.max_complexity))

    def _test_load_diff(self):
        manager = TaskManager()
        min_load = min(manager.employees, key=lambda emp: emp.load).load
        max_load = max(manager.employees, key=lambda emp: emp.load).load
        self.assertLessEqual(max_load - min_load, self.max_complexity)

    def test_manager_is_singleton(self):
        manager1 = TaskManager()
        manager2 = TaskManager()

        self.assertEqual(manager1, manager2)

    def test_manager_contains_its_data(self):
        employees = [Employee(name='task_%d' % i, cp_per_time=randint(1, 5))
                     for i in range(1, 11)]
        tasks = [Task(name='task_%d' % i, complexity=randint(1, 5)) for i in
                 range(1, 11)]
        manager = TaskManager(employees=employees, tasks=tasks)

        self.assertEqual(manager.employees, employees)
        self.assertEqual(manager.tasks, tasks)

    def test_create_employee(self):
        data = {'name': 'anyemployee', 'cp_per_time': 2}
        manager = TaskManager()

        manager.create_empoyee(**data)
        self.assertEqual(len(manager.employees), 1)
        self.assertEqual(manager.employees[0].name, data['name'])
        self.assertEqual(manager.employees[0].cp_per_time, data['cp_per_time'])

    def test_create_task(self):
        data = {'name': 'anytank', 'complexity': 2}
        manager = TaskManager()

        manager.create_task(**data)
        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(manager.tasks[0].name, data['name'])
        self.assertEqual(manager.tasks[0].complexity, data['complexity'])

    def test_manager(self):
        manager = TaskManager()
        self._create_employees(10)
        self._create_tasks(100 * 10)
        manager.manage()

        self._test_load_diff()

    def test_remanage(self):
        manager = TaskManager()
        self._create_employees(10)
        self._create_tasks(100 * 10)
        manager.manage()
        self._test_load_diff()

        self._create_employees(10)
        self._create_tasks(100 * 10)
        manager.manage()
        self._test_load_diff()

        self._create_employees(5)
        self._create_tasks(100 * 15)
        self._test_load_diff()

