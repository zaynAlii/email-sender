from agents import function_tool
from pathlib import Path
from typing import Union , Annotated
from pydantic import Field
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
from utils.utilities import load_email_configurations
# def validating_ParamsInput()
def Validating_paramInput(
    self,
    sender: str,
    recipient: str,
    body: str,
    subject: str|None=None,
   
):
    if  sender and isinstance(sender , str):
      if  recipient and isinstance(recipient , str):
        if  subject and isinstance(subject , str):
        #   if  body and isinstance(body , str):
                return True
        #   else:
        #         raise ValueError("Email body is required")
        else:
                raise ValueError("Email subject is required")
      else:    
           raise ValueError("Recipient email is required")
    else:
        raise ValueError("Sender email is required")


@function_tool
def sendFancyMail(filePath:Union[Path , str],
                  Subject:str ,
                  From:str , 
                  To:str, 
                  plainTextbody:Union[str | None] =None,
                  cc: Annotated[list[str] | None, Field(description="List of CC email addresses")] = None,
                  bcc: Annotated[list[str] | None, Field(description="List of BCC email addresses")] = None
    
                  ):
    """
    Sends an email with HTML content, and optionally plain text content, to specified recipients.

    This function reads an HTML file for the email body, attaches it, and sends the email
    via an SMTP server using SSL. It also supports CC and BCC recipients.

    Args:
        filePath (Union[Path, str]): The path to the HTML file to be used as the email body.
                                     Must be a valid path to an existing .html file.
        Subject (str): The subject line of the email.
        From (str): The sender's email address.
        To (str): The primary recipient's email address.
        plainTextbody (Union[str | None], optional): An optional plain text 
                                                    body for the email. Defaults to None.
        cc (Annotated[list[str] | None, Field(description="List of CC email addresses")], optional):
            A list of email addresses to be included in the CC field. Defaults to None.
        bcc (Annotated[list[str] | None, Field(description="List of BCC email addresses")], optional):
            A list of email addresses to be included in the BCC field. Defaults to None.

    Raises:
        ValueError: If `filePath` is not a string or Path object, is empty, does not exist,
                    or is not an HTML file.
        ValueError: If `From`, `To`, or `Subject` are missing or invalid.
        ValueError: If email body is missing.
    """
    print("==================================Fancy=======================================================")
    if not isinstance(filePath,Union[str,Path]) :
        raise ValueError(f"filePath must be either str or Path obj.    Got {type(filePath)}")
    if isinstance(filePath,Path):
        if filePath == Path("."):
            raise ValueError(f"Value  of filePath  must be not empty  Path obj  provide proper path of the .html file .Got {filePath} ")
    if isinstance(filePath ,str):    
        if not filePath:
            raise ValueError(f"Value of filePath  must be not empty str  obj . provide proper path of the .html file. Got {filePath} ")
    
        else :
            filePath:Path=Path(filePath)
    
    if not filePath.exists():
        raise ValueError(f"FilePath not exist (Error). provide the correct path . Got {filePath}")
    
    if  not filePath.suffix != ".html":
        raise ValueError(f"file must be a .html file . Got {filePath.suffix}")
    
    Validating_paramInput(From , To , plainTextbody,Subject)
    
    serverConfig:dict[str,str]=load_email_configurations()
    
    
    SMTP_SERVER=serverConfig["SMTP_SERVER"]
    SMTP_TLS_PORT=int(serverConfig["SMTP_TLS_PORT"])
    SMTP_SSL_PORT=int(serverConfig["SMTP_SSL_PORT"])
    App_PASSWORD=serverConfig["App_PASSWORD"]
    
    message = MIMEMultipart("alternative")
    
    message["Subject"]=Subject
    message["From"]=From
    message["To"]=To    
    
    Allrecipitant=[To]
    
    if cc and isinstance(cc,list):
        message["Cc"]=",".join(cc)
        Allrecipitant.extend(cc)
    
    if bcc and isinstance(bcc , list):
        Allrecipitant.extend(bcc)
    
    
    if plainTextbody:
        textPartIs=MIMEText(plainTextbody , "plain")
        message.attach(textPartIs)            
    
    with open (filePath , "r" , encoding="utf-8") as file:
        
        htmlContent=file.read()
    if not htmlContent:
        raise ValueError("Email body is required . Error  .html file is empty   ")
    
    htmlpartIs=MIMEText(htmlContent, "html")
    
    message.attach(htmlpartIs)
    
    
    context=ssl.create_default_context()
    
    with smtplib.SMTP_SSL(SMTP_SERVER ,SMTP_SSL_PORT , context=context) as server:
        server.login(From , App_PASSWORD )
        server.sendmail(From ,Allrecipitant , message.as_string() )
               
    
    
    
    
       
    