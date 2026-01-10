from pathlib import Path
from agents import function_tool



@function_tool
def createFile(fullPath:str , fileName:str):
    
    """
       Creates an MJML file inside an existing email template src directory.
       The file must end with .mjml and the path must already exist.
       
       Args : 
            fullPath:str : The full path where the file will be created.
            fileName:str : The name of the file to be created (must end with .mjml)
       
       Return : 
        str: Confirmation message including the full path of the created file.
           
    """
    
    
    print("==============================Generating File ============================================",)
    
    if not fileName or not  fileName.endswith(".mjml") or not isinstance(fileName, str):
        raise ValueError("Invalid file name. The file name must end with .mjml extension.")
    
    if not fullPath    or not isinstance(fullPath , str):
       raise ValueError("Invalid fullPath provided , it should be a non-empty string") 
       
    
    if not Path(fullPath).exists():
           raise ValueError( f"The provided path '{fullPath}' does not exist. Please provide a valid path.")    
    
    fileIs= Path(fullPath) / fileName       
    
    fileIs.touch(exist_ok=True)
    
    return f"File {fileName} has been successfully created in This directory Path  {fullPath} and full Path is {fileIs} "
    
    
    
    
    
    
    
    
    
    
    
    
    