import ast
import boto3
import base64
from botocore.exceptions import ClientError


def secret_manager():

    secret_name = "stock_price_API"
    region_name = "ap-northeast-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
    except ClientError as e:
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret_data = get_secret_value_response['SecretString']
            secret = ast.literal_eval(secret_data)
            print(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print(decoded_binary_secret)

if __name__ == "__main__":
    secret_manager()