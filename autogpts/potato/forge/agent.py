import json
import pprint

from forge.sdk import (
    Agent,
    AgentDB,
    Step,
    StepRequestBody,
    Workspace,
    ForgeLogger,
    Task,
    TaskRequestBody,
    PromptEngine,
    chat_completion_request,
)

LOG = ForgeLogger(__name__)


class ForgeAgent(Agent):
    """
    The goal of the Forge is to take care of the boilerplate code so you can focus on
    agent design.

    There is a great paper surveying the agent landscape: https://arxiv.org/abs/2308.11432
    Which I would highly recommend reading as it will help you understand the possabilities.

    Here is a summary of the key components of an agent:

    Anatomy of an agent:
         - Profile
         - Memory
         - Planning
         - Action

    Profile:

    Agents typically perform a task by assuming specific roles. For example, a teacher,
    a coder, a planner etc. In using the profile in the llm prompt it has been shown to
    improve the quality of the output. https://arxiv.org/abs/2305.14688

    Additionally baed on the profile selected, the agent could be configured to use a
    different llm. The possabilities are endless and the profile can be selected selected
    dynamically based on the task at hand.

    Memory:

    Memory is critical for the agent to acculmulate experiences, self-evolve, and behave
    in a more consistent, reasonable, and effective manner. There are many approaches to
    memory. However, some thoughts: there is long term and short term or working memory.
    You may want different approaches for each. There has also been work exploring the
    idea of memory reflection, which is the ability to assess its memories and re-evaluate
    them. For example, condensting short term memories into long term memories.

    Planning:

    When humans face a complex task, they first break it down into simple subtasks and then
    solve each subtask one by one. The planning module empowers LLM-based agents with the ability
    to think and plan for solving complex tasks, which makes the agent more comprehensive,
    powerful, and reliable. The two key methods to consider are: Planning with feedback and planning
    without feedback.

    Action:

    Actions translate the agents decisions into specific outcomes. For example, if the agent
    decides to write a file, the action would be to write the file. There are many approaches you
    could implement actions.

    The Forge has a basic module for each of these areas. However, you are free to implement your own.
    This is just a starting point.
    """

    def __init__(self, database: AgentDB, workspace: Workspace):
        """
        The database is used to store tasks, steps and artifact metadata. The workspace is used to
        store artifacts. The workspace is a directory on the file system.

        Feel free to create subclasses of the database and workspace to implement your own storage
        """
        super().__init__(database, workspace)

    async def create_task(self, task_request: TaskRequestBody) -> Task:
        """
        The agent protocol, which is the core of the Forge, works by creating a task and then
        executing steps for that task. This method is called when the agent is asked to create
        a task.

        We are hooking into function to add a custom log message. Though you can do anything you
        want here.
        """
        task = await super().create_task(task_request)
        LOG.info(
            f"📦 Task created: {task.task_id} input: {task.input[:40]}{'...' if len(task.input) > 40 else ''}"
        )
        return task

    async def execute_step_clone(self, task_id: str, step_request: StepRequestBody) -> Step:
        """
        For a tutorial on how to add your own logic please see the offical tutorial series:
        https://aiedge.medium.com/autogpt-forge-e3de53cc58ec

        The agent protocol, which is the core of the Forge, works by creating a task and then
        executing steps for that task. This method is called when the agent is asked to execute
        a step.

        The task that is created contains an input string, for the bechmarks this is the task
        the agent has been asked to solve and additional input, which is a dictionary and
        could contain anything.

        If you want to get the task use:

        ```
        task = await self.db.get_task(task_id)
        ```

        The step request body is essentailly the same as the task request and contains an input
        string, for the bechmarks this is the task the agent has been asked to solve and
        additional input, which is a dictionary and could contain anything.

        You need to implement logic that will take in this step input and output the completed step
        as a step object. You can do everything in a single step or you can break it down into
        multiple steps. Returning a request to continue in the step output, the user can then decide
        if they want the agent to continue or not.
        """
        # An example that
        step = await self.db.create_step(
            task_id=task_id, input=step_request, is_last=True
        )

        self.workspace.write(task_id=task_id, path="output.txt", data=b"Washington D.C")

        await self.db.create_artifact(
            task_id=task_id,
            step_id=step.step_id,
            file_name="output.txt",
            relative_path="",
            agent_created=True,
        )

        step.output = "Washington D.C"

        LOG.info(f"\t✅ Final Step completed: {step.step_id}")

        return step

    async def execute_step(self, task_id: str, step_request: StepRequestBody) -> Step:

        print("Task ID:")
        pprint.pprint(task_id)
        print("Step Request:")
        pprint.pprint(step_request)

        if not step_request.input:
            steps = (await self.db.list_steps(task_id))[0]
            LOG.info(f"Found {steps} from db")
            # find first step without output
            # step = next((step for step in steps if not step.status == "done"), None)
            step = steps[-1]
            LOG.info(f"Found {step} from db")
        else:
            step = await self.db.create_step(
                task_id=task_id, input=step_request, is_last=False
            )
        prompt_engine = PromptEngine("gpt-3.5-turbo")
        system_prompt = prompt_engine.load_prompt("system-format")

        messages = [
            {"role": "system", "content": system_prompt},
        ]
        task_kwargs = {
            "task": step.input,
            "abilities": self.abilities.list_abilities_for_prompt(),
        }
        task_prompt = prompt_engine.load_prompt("task-step", **task_kwargs)
        messages.append({"role": "user", "content": task_prompt})
        # print task
        print("Prompt:")
        pprint.pprint(messages)

        chat_response = await chat_completion_request(messages, model="gpt-3.5-turbo")
        raw_answer = chat_response["choices"][0]["message"]["content"]
        # print
        print("Raw Answer:")
        pprint.pprint(raw_answer)

        answer = json.loads(raw_answer)
        ability = answer["ability"]
        # print answer and ability
        print("Answer:")
        pprint.pprint(answer)
        print("Ability:")
        pprint.pprint(ability)
        if ability["name"] == "write_file":
            step.is_last = True

        output = await self.abilities.run_ability(
            task_id, ability["name"], **ability["args"]
        )
        print("Output:")
        pprint.pprint(output)

        if ability["name"] == "read_file":
            additional_input = {"file_content": str(output), "ability": ability}

        step.output = answer["thoughts"]["speak"]

        LOG.info(f"Update {step} to done")
        await self.db.update_step(task_id, step.step_id, "done")

        message = f"\t🔄 Step executed: {step.step_id} input: {step.input}"
        if step.is_last:
            message = (
                f"\t✅ Final Step completed: {step.step_id} input: {step.input}"
            )
        else:
            step_request.input = step_request.input + json.dumps(additional_input)
            next_step = await self.db.create_step(
                task_id=task_id, input=step_request, is_last=False
            )
            LOG.info(f"Created next step {next_step}")

        LOG.info(message)

        # artifact = await self.db.create_artifact(
        #     task_id=task_id,
        #     step_id=step.step_id,
        #     file_name="output.txt",
        #     relative_path="",
        #     agent_created=True,
        # )

        return step
