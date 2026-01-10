from agents import Agent
from  utils import PromptManager
from pathlib import Path
from utils import load_LLM_configurations
from agents import OpenAIChatCompletionsModel
from agents.extensions.models.litellm_model import LitellmModel
from agents import ModelSettings
class MJMLGenerator():
    def __init__(self , modelIs:LitellmModel) -> None:
        
        self.prompt_manager=PromptManager(Path(__file__).parent.parent.parent / "Prompt" / "agentPrompts.yaml")
        self.modelIs=modelIs
    # 
    # @property
    # def  modelIs(self)->str:
    #     modelIs=load_LLM_configurations() ["model_name"]
    #     return 
     
    
    @property
    def agentIs(self)->Agent:   
        mjmlGeneratorIs=Agent(
            name="MJML Generator",
            instructions=self.prompt_manager.render_prompt("agent.Tool.MjmlAgent.system_prompt"), 
            # model_settings=ModelSettings(max_tokens=7177),                          
            model=self.modelIs
        )
        
        return mjmlGeneratorIs
        
        
    
    