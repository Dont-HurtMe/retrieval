from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    port: int = 8000
    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: str | None = None
    collection_name: str = "knowledge_base"
    model_name: str = "BAAI/bge-m3"
    s3_endpoint_url: str = ""
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_bucket_name: str = "knowledge-base"
    class Config:
        env_file = ".env"
        extra = "ignore" 
        
settings = Settings()