class Dispatcher:
    def __init__(self):
        self.agent_registry = {}

    def register_agent(self, task_type, agent):
        self.agent_registry[task_type] = agent

    def run(self, context):
        agent = self.agent_registry.get(context.task_type)
        if agent:
            result = agent.run(context.params)
            context.results[context.task_type] = result
        else:
            print(f"No agent registered for task type: {context.task_type}")
        return context
