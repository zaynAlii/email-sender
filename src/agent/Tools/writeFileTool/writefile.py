from agents import function_tool
from pathlib import Path

# from 

@function_tool
def writeMjml(pathToFile:str, content:str):
    """
    Writes MJML (Mailjet Markup Language) content to an existing file on disk.

    This tool is intended for use by an agent that generates email templates
    using MJML markup. The agent should first generate valid MJML code as a
    string, then call this tool to persist that markup into a `.mjml` file.

    The file path must already exist. This tool does NOT create directories
    or files; it only writes content to an existing file.

    Args:
        pathToFile (str):
             relative path to an existing `.mjml` file where the
            MJML markup should be written.

        content (str):
            The complete MJML markup to write into the file. This should be
            valid MJML syntax (e.g., <mjml>, <mj-body>, <mj-section>, etc.).

    Behavior:
        - Overwrites the entire contents of the target file.
        - Writes using UTF-8 encoding.
        - Validates input types and ensures non-empty values.
        - Raises errors if the file path does not exist or inputs are invalid.

    Returns:
        str:
            A confirmation message indicating the MJML file was written
            successfully.

    Raises:
        ValueError:
            - If `pathToFile` is not a string or is empty.
            - If `content` is not a string or is empty.
            - If the specified file path does not exist.

    Example:
        The agent generates MJML markup and saves it:

        writeMjml(
            pathToFile="templates/welcome_email.mjml",
            content="<mjml><mj-body>...</mj-body></mjml>"
        )
        """
        
    print("=====================================Write File =======================================")    
    if not isinstance(pathToFile,str):
        raise ValueError(f"pathToFile  must be a string type , Got{type(pathToFile)}")
    if not pathToFile:
        raise ValueError(f"pathToFile  must be a  non emptry string  , Got{pathToFile}")
    if not isinstance(content , str):
        raise ValueError(f"content  must be a string type , Got{type(content)}")
    if not content:
        raise ValueError(f"content  must be a  non emptry string  , Got{content}")
    
    pathToFile:Path=Path(pathToFile)
    if not pathToFile.exists():
        raise ValueError(f"Error - Path not exist , provide correct path. Got({pathToFile}) ")
    
    with open(pathToFile,'w' , encoding="utf-8")as f:
        f.write(content)
    
    
    # if not pathToFile.is_file():
        # raise f""
    
    return f"File has been written successfully To this Path {pathToFile} "    
            
