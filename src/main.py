import sys 
import os
import config
from agent import LLMConfig

from handler import AgentHandler


async def main():
    try:
        configIs:dict[str,str]={
            "LLM_BASE_URL":config.LLM_BASE_URL,
            "LLM_API_KEY":config.LLM_API_KEY,
            "LLM_MODEL":config.LLM_MODEL,
            
        }
        llm_config=LLMConfig(**configIs)
        # print(llm_config)
        execution=AgentHandler(llm_config)
        await execution.handle()
        
        
    except Exception as e:
        raise ValueError(f"Error in main : {e}")    
        
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
        
    