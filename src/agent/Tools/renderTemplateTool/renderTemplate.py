from agents import function_tool
from typing import Union , Any
from pathlib import Path
import jinja2
from jinja2 import FileSystemLoader
import mjml
from mjml import mjml2html
from agents import RunContextWrapper
def  handling_tool_error(ctx:RunContextWrapper, error :Exception):
    
    print("Error has occured")
    print("ErroIs The error is ->",error)
    return "Please stop calling tool , tool program has crashed and convey this mesg to real user  ! thanks"


@function_tool 
def renderMjmlwithData(template_Path:str , FileName:str  , data):
    """
    Render MJML template with data.

    Args:
        template_Path (str): Path to the directory containing MJML template files.
        FileName (str): The name of the MJML template file within the template directory.
        data (dict[str, Any]): Data to render in the template.

    Returns:
        str: Path to the compiled HTML file.

    Raises:
        ValueError: If `template_Path`, `FileName`, or `data` are invalid or empty.
        RuntimeError: If MJML compilation fails.
    """
    print("========================================Render=============================================")
    if not template_Path :
        raise ValueError("mjmlFilePath must be  a not empty str")
    
    if not isinstance(template_Path,str): 
        typeis=type(template_Path)
        raise ValueError(f" This {template_Path} must be a str. Got Type {typeis}  ")
    # if not mjmlFilePath.endswith(".mjml"):
    #   raise ValueError(f"mjmlFilePath must end with .mjml ext . Got {mjmlFilePath}")
    
    if not FileName :
        raise ValueError("FileName must be  a not empty str")
    if not isinstance(FileName,str): 
        typeis=type(FileName)
        raise ValueError(f" This {FileName} must be a str. Got Type {typeis}  ")
    if not FileName.endswith(".mjml"):
      raise ValueError(f"Filename must end with .mjml ext . Got {FileName}")
    
    if not isinstance(data,dict):
        raise ValueError(f"Data must be a dictionary")
    
    if not data:
        raise ValueError("Data dict must not empty. Got empty dict ")
    
    htmlFilePathIs:Path=Path(template_Path).parent / "build" / FileName.replace(".mjml",".html")       
  
    env=jinja2.Environment(loader=FileSystemLoader(template_Path))
    
    template = env.get_template(FileName)
    
    renderedTemplateIs=template.render(data)
    
    try : 
       ...
       result=mjml2html(renderedTemplateIs)
       
       with open(htmlFilePathIs , 'w' , encoding="utf-8") as file:
           file.write(result)
       
       if htmlFilePathIs.is_file():
           return f"Data rendered In mjml template and successfully compiled to .html  soo The Path to the compiled Html File {htmlFilePathIs}" 
    except Exception as e:
        raise RuntimeError(f"MJML Compilation Failed: {str(e)}")
            
    
    
         
    
    
    
    
    
    
    
    
    