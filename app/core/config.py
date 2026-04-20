from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    port: int
    qdrant_url: str
    qdrant_api_key: str | None = None 
    collection_name: str
    model_name: str
    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str  
    llm_api_base_url: str  
    llm_api_key: str
    llm_model: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()