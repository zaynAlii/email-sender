from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml
import jinja2
from copy import copy
class PromptManager:
    def __init__(self, file_path: Union[str, Path], section_path: Optional[str] = None) -> None:
        """Initialize the prompt manager with a YAML file path.
           Manages loading and rendering of prompts from YAML files
        Args:
            file_path: Path to the YAML file containing prompts
            section_path: Section of the file to load prompts from (supports dot notation for nested keys)

        Raises:
            FileNotFoundError: If the prompt file doesn't exist
            yaml.YAMLError: If the YAML file is malformed
            ValueError: If the section is not found in the prompts file
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self._prompt_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse YAML file {file_path}: {e}")

        if section_path:
          ...
          
          
    def  load_PromptsFile()->dict[str , Any]:
        ...      
    def _traverse_Path(self , data:dict , path:str):
        current = data

        try:
            for key in path.split("."):
                current = current[key]
        except (KeyError, TypeError):
            raise ValueError(f"Path '{path}' not found in prompts data")

        return current      
    
    def _load_prompt(self, prompt_name: str) -> Union[str, Dict[str, Any]]:
        """Load a prompt from the YAML data.

        Args:
            prompt_name: Key to load prompt from (supports dot notation for nested keys)    

        Returns:
            The prompt value (string or dictionary)

        Raises:
            ValueError: If the prompt is not found
        """
        try :
           prompt_value = self._traverse_Path(self._prompt_data, prompt_name)
        
        except ValueError as e:
            raise ValueError(f"Prompt '{prompt_name}' not found in prompts data")
        return copy(prompt_value)    
    
    
    def render_prompt(self, prompt_name: str) -> str:
        """Render a prompt template 

        Args:
            prompt_name: Key to load prompt from (supports dot notation for nested keys)

        Returns:
            The rendered prompt string

        Raises:
            ValueError: If the prompt is not found or is not a string
        """
        prompt_template = self._load_prompt(prompt_name)

        if not isinstance(prompt_template, str):
            raise ValueError(f"Prompt '{prompt_name}' is not a string and cannot be rendered")
        return prompt_template
        
        # template = jinja2.Temp 

    # def render_prompt(self, prompt_name: str, context: Optional[Dict[str, Any]] = None) -> str:
    #     """Render a prompt template with the given context.

    #     Args:
    #         prompt_name: Key to load prompt from (supports dot notation for nested keys)
    #         context: Dictionary of values to render the template with

    #     Returns:
    #         The rendered prompt string

    #     Raises:
    #         ValueError: If the prompt is not found or is not a string
    #     """
    #     prompt_template = self._load_prompt(prompt_name)

    #     if not isinstance(prompt_template, str):
    #         raise ValueError(f"Prompt '{prompt_name}' is not a string and cannot be rendered")

    #     if prompt_name not in self._template_cache:
    #         self._template_cache[prompt_name] = jinja2.Template(prompt_template)

    #     template = self._template_cache[prompt_name]
    #     rendered_prompt = template.render(context or {})

    #     return rendered_prompt

