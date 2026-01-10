from agent import LLMConfig
from agent import EmailAgent
import abc



class AbstractHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self,) :
        pass
    


class AgentHandler(AbstractHandler):
    def __init__(self,  config:LLMConfig) -> None:
        self._agent_config = config
        self._agent = EmailAgent(self._agent_config)
    
    async  def handle(self):
        print("Agent Handler is handling the request")
        result = await self._agent.run()
    




