import io
import boto3
import pandas as pd
from botocore.client import Config
from typing import List, Dict
from app.core.config import settings

def fetch_parquet_texts(prefix_path: str) -> List[Dict]:
    if not prefix_path:
        return []
    endpoint = settings.s3_endpoint_url
    if not endpoint.startswith(('http://', 'https://')):
        endpoint = f"http://{endpoint}"
    s3_client = boto3.client('s3',
        endpoint_url=endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        config=Config(signature_version='s3v4')
    )
    pages_list = []
    bucket = settings.s3_bucket_name
    prefix = f"{prefix_path}/" if not prefix_path.endswith('/') else prefix_path
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' not in response:
            print(f"[Storage] No files found in {prefix}")
            return []
        for obj in response['Contents']:
            if obj['Key'].endswith('.parquet'):
                file_obj = s3_client.get_object(Bucket=bucket, Key=obj['Key'])
                df = pd.read_parquet(io.BytesIO(file_obj['Body'].read()))
                if 'text' in df.columns:
                    for _, row in df.iterrows():
                        pages_list.append({
                            "page": int(row.get('page_number', 0)),
                            "text": str(row.get('text', '')).strip()
                        })
        pages_list = sorted(pages_list, key=lambda x: x['page'])
        return pages_list
    except Exception as e:
        print(f"❌ [Storage] Error fetching parquet from {prefix}: {str(e)}")
        return []