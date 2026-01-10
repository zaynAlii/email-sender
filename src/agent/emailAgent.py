from agents import Agent , Runner , RunConfig  , AsyncOpenAI , OpenAIChatCompletionsModel , set_tracing_disabled
from dotenv import load_dotenv
import os 
import sys
from pathlib import Path
from pydantic import BaseModel , Field
from utils import PromptManager
from .Tools import MJMLGenerator , sendEmail , createFile , createFolder , renderMjmlwithData , sendFancyMail , writeMjml
from agents.extensions.models.litellm_model import LitellmModel 
from agents import SQLiteSession
# from agents import ModelSettings


set_tracing_disabled(True)
# Get the project root automatically
# current_file = Path(__file__).resolve()
# print(current_file)
# src_dir = current_file.parent.parent  # Go up: agent → src
# project_root = src_dir.parent         # Go up: src → project_root

# Add both to Python path
# sys.path.insert(0, str(project_root))
# sys.path.insert(0, str(src_dir))

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from utils import load_configurations
# load_dotenv()
# print("Hello")
# config =load_configurations()
# print(LLM_BASE_URL)

  
# class GmaailAppPassword(BaseModel):
    # app_password: str = Field(..., description="App password for Gmail authentication")

class LLMConfig(BaseModel):
    LLM_BASE_URL: str = Field(..., description="Base URL for the LLM service")
    LLM_MODEL: str = Field(..., description="Model name for the LLM")
    LLM_API_KEY: str = Field(..., description="API key for accessing the LLM service")

class EmailAgent():
    def __init__(self, agent_config: LLMConfig):
        self._agent_config = agent_config.model_dump()
        
        self._promptManager = PromptManager(file_path=Path(__file__).parent/"Prompt"/"agentPrompts.yaml")
        
    
    async def run(self):
        ...
        # SystemPromptForAgent=self._promptManager._load_prompt("agent.Email_Agent.system_prompt")
        
        agentIs=self._Email_agent
        sessionIs=self._get_session
             
        while True:
            
            userInput:str =input("Enter your email request: ")
            if userInput.lower() in ["exit" , "quit" , "e" , "q"]:
                break
            
            result=await Runner.run(
                agentIs,
                userInput,    
                session=sessionIs
                )
            
            print(result.final_output)
                
        
        
    
    @property
    def _get_session(self):
        return SQLiteSession("conversation_123")    
        
        
    @property
    def _get_client(self):
        
        minimax_client= AsyncOpenAI(
            base_url=self._agent_config["LLM_BASE_URL"],
            api_key=self._agent_config["LLM_API_KEY"],
            )
        minimax_server=OpenAIChatCompletionsModel(
            client=minimax_client,
            model=self._agent_config["LLM_MODEL"]
        )
        
        return minimax_client , minimax_server
    
    
    @property
    def _Email_agent(self):
        # client , model_server = self._get_client
        
        mjml_generatorAgent=MJMLGenerator(modelIs=LitellmModel(model=self._agent_config["LLM_MODEL"] , api_key=self._agent_config["LLM_API_KEY"])).agentIs
        
        return Agent(
            name="Email Agent",
            instructions=self._render_prompt("agent.Email_Agent.system_prompt"),
            # model_settings=ModelSettings(max_tokens=7177),
            model=LitellmModel(model=self._agent_config["LLM_MODEL"] , api_key=self._agent_config["LLM_API_KEY"]),
            tools=[
                   sendEmail,
                   mjml_generatorAgent.as_tool(
                       tool_name="MJML_markup_Generator",
                       tool_description=""" You are an expert MJML email template generator.

          Your task:
          - Generate VALID MJML code for email templates.
          - Output ONLY MJML (no explanations, no markdown, no comments).
          - The MJML must be ready to compile using the official MJML compiler.
          - The MJML must be compatible with Jinja2 templating syntax.

          Rules:
          1. Use ONLY MJML tags (mjml, mj-body, mj-section, mj-column, mj-text, mj-button, mj-image, mj-divider, mj-spacer).
          2. Do NOT use raw HTML unless wrapped inside <mj-raw> (use this only if absolutely necessary).
          3. Use inline styling via MJML attributes (font-size, color, padding, background-color).
          4. Ensure the email is responsive and compatible with Gmail, Outlook, Yahoo.
          5. Avoid JavaScript, external CSS, and unsupported CSS properties.
          6. Use Jinja2 placeholders like {{ variable_name }} for dynamic content.
          7. Use Jinja2 control blocks when requested:
            - {% if condition %}
            - {% for item in items %}
          8. Keep layout clean, professional, and readable.
          9. Do NOT hardcode text that the user wants dynamic.
          10. Output must start with <mjml> and end with </mjml>.

          Input you will receive:
          - Email purpose (e.g., welcome, invoice, alert)
          - Tone (professional, friendly, marketing)
          - Content requirements (headings, buttons, images, links)
          - Variables to include (names, links, OTPs, etc.)"""
                       ),
                   renderMjmlwithData,
                   createFile,
                   createFolder,
                   sendFancyMail      ,
                   writeMjml    
                ],
        )
        
    def _render_prompt(self, prompt_name: str):
         
         return self._promptManager._load_prompt(prompt_name)
        
    
    


