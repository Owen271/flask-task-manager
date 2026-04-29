import csv

class Task:
    def __init__(self, id: int, title, priority, due, status: bool):
        self.id = id
        self.title = title
        self.priority = priority
        self.due = due
        self.status = status
        
    def __str__(self):
        status = "Complete" if self.status else "Incomplete"
        return f"{self.id} | {self.title} | {self.priority} | {self.due} | {status}"

class TaskManager:
    def __init__(self, tasks = None):
        self.tasks = tasks if tasks else {}
        self.next_id = 1

    def add_task(self, title: str, priority: str, due: str):
        task = Task(self.next_id, title, priority, due, False)
        self.tasks[self.next_id] = task
        self.next_id += 1

    def del_task(self, id: int):
        if id in self.tasks:
            del self.tasks[id]
            return True
        else:
            return False

    def list_tasks(self):
        for task in self.tasks.values():
            yield(task)

    def complete_task(self, id: int):
        if id in self.tasks:
            self.tasks[id].status = True
            return True
        else:
            return False

    def search_tasks(self, query: str):
        for task in self.tasks.values():
            if query.strip().lower() in task.title.strip().lower():
                yield(task)

    def edit_task(self, id: int, title: str, priority: str, due: str):
        self.tasks[id].title = title
        self.tasks[id].priority = priority
        self.tasks[id].due = due


    def loadcsv(self):
        try:
            with open("task1.csv", 'r', newline = '', encoding = 'utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:

                    task = Task(int(row['id']), row['title'], row['priority'], row['due'], row['status']=="True")
                    self.tasks[task.id] = task
                
        except FileNotFoundError:
            return

        if self.tasks:
            self.next_id = max(self.tasks) + 1

    def savecsv(self):
        with open("task1.csv", 'w', newline = '', encoding = 'utf-8') as f:
            writer = csv.writer(f)

            writer.writerow(["id", "title", "priority", "due", "status"])
            for task in self.tasks.values():
                writer.writerow([task.id, task.title, task.priority, task.due, task.status])