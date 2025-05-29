import json
from google.adk.models.lite_llm import LiteLlm
import boto3

secret_manager = boto3.client('secretsmanager', region_name='us-east-1')


def get_secret_val(key: str):
    secret = secret_manager.get_secret_value(SecretId='ais-aiservices-api-dev')
    secret_dict = json.loads(secret['SecretString'])
    return secret_dict[key]


azure_llm = LiteLlm(
    model='azure/gpt-4o',
    api_base=get_secret_val('AZURE_ENDPOINT'),
    api_version='2024-12-01-preview',
    api_key=get_secret_val('AZURE_NEW_KEY')
)
