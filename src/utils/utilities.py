from dotenv import load_dotenv
import os 
load_dotenv()

# def load_LLM_configurations()->dict[str , str]:
#     configurations = {
       
#         "LLM_BASE_URL": os.environ["LLM_BASE_URL"],
#         "LLM_MODEL": os.environ["LLM_MODEL"],
#         "LLM_API_KEY": os.environ["LLM_API_KEY"],
        
#     }
#     return configurations
  
def load_email_configurations()->dict[str , str]:
    configurations = {
        "App_PASSWORD": os.environ["App_PASSWORD"],
        "SMTP_SERVER": os.environ["SMTP_SERVER"],
        "SMTP_TLS_PORT": os.environ["SMTP_TLS_PORT"],
        "SMTP_SSL_PORT":os.environ["SMTP_SSL_PORT"]
    }
    return configurations  