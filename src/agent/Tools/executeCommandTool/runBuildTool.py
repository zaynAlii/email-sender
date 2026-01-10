from agents import function_tool

from pathlib import Path
import subprocess

ALLOWED_COMMANDS={
    "mjml":["mjml"]
}


@function_tool
def makeBuildTool(mjmlFile:Path , htmlFile:Path , commandName:str="mjml" ):
    
    """
    Compiles an MJML file to an HTML file using an external command.

    This function takes a source MJML file and a destination path, then uses the
    specified command-line tool to compile the MJML into standard HTML. It validates
    the input and output files and handles the subprocess execution.

    Args:
        mjmlFile (Path): The path to the input .mjml file.
        htmlFile (Path): The path where the output .html file will be saved.
        commandName (str, optional): The name of the command to use (e.g., "mjml").
            Defaults to "mjml".

    Returns:
        Path: The path to the generated HTML file.

    Raises:
        ValueError: If input files are invalid or the command is not allowed.
        RuntimeError: If the compilation process fails.
        FileNotFoundError: If the specified command is not found.
    """
    
    print("===================================Build============================================")
    if not isinstance(mjmlFile,Path): 
        TypeIs=type(mjmlFile)
        raise ValueError(f"mjmlFile  must be a Path object. Got: {mjmlFile} type {TypeIs} ") 
    
    
    
    
    if  not mjmlFile.is_file():
        raise ValueError(f"File NOt exist . mjmlFile must be a file that exists . Got {mjmlFile}.  ")
    
    if  not mjmlFile.suffix!=".mjml":
        raise ValueError(f"mjmlFile must be a valid .mjml file. Got: {mjmlFile.suffix}") 
        
    if not isinstance(htmlFile,Path):
          raise ValueError(f"htmlFile must be a Path object. Got: {type(htmlFile)}")
              
    if  not htmlFile.suffix!=  ".html":
        raise ValueError(f"htmlFile must have a .html extension. Got : {htmlFile.suffix}") 
    
    
    if commandName not in ALLOWED_COMMANDS :
        raise ValueError (f"Command Name is not found in Allowed Commands {ALLOWED_COMMANDS}  ")    
    
    command_parts:list[str]=ALLOWED_COMMANDS[commandName].copy()
    nextArgs:list[str]=[str(mjmlFile) , "-o" , str(htmlFile)]
    command_parts.extend(nextArgs)
    try:
        
    # fullCommandIs:list[str]=
        result= subprocess.run(
            command_parts,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    
    except FileNotFoundError :
        # This is raised if the 'mjml' command itself is not found in the system's PATH
      
            raise FileNotFoundError(f"The command '{commandName}' was not found. Please ensure it is installed.")
    except subprocess.CalledProcessError as e:
        # This is raised because `check=True` was used and the command returned a non-zero exit code
         raise RuntimeError(f"Compilation failed. Error: {e.stderr}")
        
    # if result.returncode != 0:
    #     raise RuntimeError(f"By running the Error  , just got error . The Error Is {result.stderr}")
    
    if not htmlFile.is_file():
          raise RuntimeError(f"Compilation succeeded, but the output file was not created: {htmlFile}")
    
    return f"Command Succesfully Ran and file has been compiled to .html extension {htmlFile}"
 
    
    
    
   