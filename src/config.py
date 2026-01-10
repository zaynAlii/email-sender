import os 

import dotenv


from dotenv import load_dotenv


load_dotenv()



def str_to_bool(value:str) -> bool:
    
    if value.lower() in ["true" , "1" ,"yes","y"]:
       return True
    elif value.lower() in ["false" , "0" ,"no","n"]:
       return False
    
    else :
        raise ValueError(f"Invalid boolean value: {value}")
    
    
    
LLM_BASE_URL=os.environ["LLM_BASE_URL"]
LLM_API_KEY=os.environ["LLM_API_KEY"]
LLM_MODEL=os.environ["LLM_MODEL"]
    
