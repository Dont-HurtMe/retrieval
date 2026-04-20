import dspy
import litellm
import httpx
from openai import OpenAI
from app.core.config import settings

def configure_dspy():
    litellm.ssl_verify = False
    custom_http_client = httpx.Client(verify=False)
    
    custom_openai_client = OpenAI(
        base_url=settings.llm_api_base_url, 
        api_key=settings.llm_api_key,
        http_client=custom_http_client
    )

    lm = dspy.LM(
        model=settings.llm_model,
        client=custom_openai_client,
        cache=False,
        timeout=120,
        max_tokens=4096
    )

    dspy.configure(lm=lm)
    return lm