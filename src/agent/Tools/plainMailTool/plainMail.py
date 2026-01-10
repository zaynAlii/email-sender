from utils import  load_email_configurations
import smtplib
from  email.message  import EmailMessage
import ssl
from typing import Annotated ,Any
from agents import function_tool
from pydantic import BaseModel , Field
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import  Path
from typing import Union
# class PlainMail:
    
     

def CheckValidation(
    sender: str,
    recipient: str,
    subject: str,
    body: str,
   
):
    if  sender and isinstance(sender , str):
      if  recipient and isinstance(recipient , str):
        if  subject and isinstance(subject , str):
          if  body and isinstance(body , str):
                return True
          else:
                raise ValueError("Email body is required")
        else:
                raise ValueError("Email subject is required")
      else:    
           raise ValueError("Recipient email is required")
    else:
        raise ValueError("Sender email is required")




@function_tool
    
def sendEmail(
    From:str ,
    To:str ,
    Subject:str,
    body:str,
    attachment_path:Path|str|None=None,
    cc: list | None = None,
    bcc: list | None= None
        ):
    """
    Sends a plain text email, with optional attachments and support for CC/BCC.

    This function constructs and sends an email using an SMTP server with SSL. It supports
    attaching a single file and includes validation for email parameters and attachment paths.

    Args:
        From (str): The sender's email address.
        To (str): The primary recipient's email address.
        Subject (str): The subject line of the email.
        body (str): The plain text content of the email.
        attachment_path (Annotated[Path | str | None, "Attachemnt can be any pdf , doc , jpg , png"], optional):
            The path to an optional file attachment. Supported formats include PDF, DOC, DOCX, JPG, PNG, JPEG.
            Defaults to None.
        cc (Annotated[list[str] | None, Field(description="List of CC email addresses")], optional):
            A list of email addresses to be included in the CC field. Defaults to None.
        bcc (Annotated[list[str] | None, Field(description="List of BCC email addresses")], optional):
            A list of email addresses to be included in the BCC field. Defaults to None.

    Raises:
        ValueError: If `From`, `To`, `Subject`, or `body` are empty or invalid.
        ValueError: If `attachment_path` is provided but does not exist, is a directory,
                    or is an unsupported file type.
    """
        # def send_email(recipient: str, subject: str, body: str, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):    # Logic to send a plain text email              
    CheckValidation(From , To , Subject , body  )    
    # return {
    # "success": True,
    # "message": "Email has been transmitted successfully"
    #  }
    mailConfig:dict[str,str]=load_email_configurations()
    
    SMTP_SERVER=mailConfig["SMTP_SERVER"]
    SMTP_TLS_PORT=int(mailConfig["SMTP_TLS_PORT"])
    SMTP_SSL_PORT=int(mailConfig["SMTP_SSL_PORT"])
    App_PASSWORD=mailConfig["App_PASSWORD"]
    # if cc and isinstance(cc,list):
    #     pass
    AllRecipients=[To]
    context = ssl.create_default_context()
    if attachment_path and isinstance(attachment_path,Union[str,Path]): 
        if isinstance(attachment_path,str):
            attachment_path=Path(attachment_path)
        if not attachment_path.exists():
            raise ValueError("Attachment Path does not exist please provide the correct Path")   
        if attachment_path.is_dir():
            raise ValueError("Attachment Path is a directory please provide the file Path")     
        
        if attachment_path.suffix.lower() not in [".pdf" , ".doc" , ".docx" , ".jpg" , ".png" , ".jpeg" ]:
            raise ValueError("Attachment Path is not a valid file type please provide the correct Path")   
        # Create a multipart message and set headers
        message=MIMEMultipart()
        message['From'] = From
        message['To'] = To
        message['Subject'] = Subject
        
        # AllRecipients=[To]
        if cc and isinstance(cc,list):
            message['Cc'] = ",".join(cc)            
            AllRecipients.extend(cc)
            # pass
        
            
        if bcc and isinstance(bcc,list):
            AllRecipients.extend(bcc)
            
        plainTextBodyIs=MIMEText(body , "plain")
        message.attach(plainTextBodyIs)
        
        with open(attachment_path, "rb") as attachment:
            part=MIMEBase("application" , "octet-stream")
            part.set_payload(attachment.read())
    
        
        encoders.encode_base64(part)
        
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={attachment_path.name}",
        )
        
        
        message.attach(part)
        
        with smtplib.SMTP_SSL(SMTP_SERVER , SMTP_SSL_PORT ,context=context ) as servre :
            servre.login(From,App_PASSWORD)
            servre.sendmail(From, AllRecipients,message.as_string())
            
        return f"Email sent   {To} with attachment name Is {attachment_path.name}"  
    else :  
            
        email_message = EmailMessage()

        email_message['From'] = From
        email_message['To'] = To
        email_message['Subject'] = Subject
        
         
        if cc and isinstance(cc, list):
            message["Cc"]=",".join(cc)
            AllRecipients.extend(cc)
        
        if bcc and isinstance(bcc,list):
            AllRecipients.extend(bcc)    
        
        email_message.set_content(body)
        with smtplib.SMTP_SSL(SMTP_SERVER,SMTP_SSL_PORT, context=context) as server:
            
            server.login(From, App_PASSWORD)
            server.sendmail(From, AllRecipients, email_message.as_string())
        return f"Email sent successfully to {To} with subject '{Subject}'"       