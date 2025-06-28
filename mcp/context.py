class TaskContext:
    def __init__(self, task_type, params):
        self.task_type = task_type
        self.params = params
        self.results = {}
