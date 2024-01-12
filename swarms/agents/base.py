from typing import Dict, List


class AbstractAgent:
    """(In preview) An abstract class for AI agent.

    An agent can communicate with other agents and perform actions.
    Different agents can differ in what actions they perform in the `receive` method.

    Agents are full and completed:

    Agents = llm + tools + memory


    """

    def __init__(
        self,
        name: str,
        # tools: List[Tool],
        # memory: Memory
    ):
        """
        Args:
            name (str): name of the agent.
        """
        # a dictionary of conversations, default value is list
        self._name = name
        self._tools = []
        self._memory = None

    @property
    def name(self):
        """Get the name of the agent."""
        return self._name

    def tools(self, tools):
        """Initialize the tools for the agent."""
        # TODO: Implement the logic to initialize the tools

    def memory(self, memory_store):
        """init memory"""
        pass

    def reset(self):
        """Reset the agent."""
        # TODO: Implement the logic to reset the agent
        """(Abstract method) Reset the agent."""

    def run(self, task: str): # Add a parameter to the run method
        """Run the agent once. Add a parameter to the method."""

    def _arun(self, taks: str):
        """Run Async run"""

    def chat(self, messages: List[Dict]):
        """Chat with the agent"""
        # TODO: Implement the logic to chat with other agents

    def _achat(self, messages: List[Dict]):
        """Asynchronous Chat"""

    def step(self, message: str):
        """Step through the agent"""
        # TODO: complete the step logic

    def _astep(self, message: str):
        """Asynchronous step"""
