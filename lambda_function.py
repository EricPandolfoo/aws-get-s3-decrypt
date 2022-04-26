import json
import boto3
import urllib
import os
import base64

from base64 import b64decode


##Clients
s3_client = boto3.client('s3')
kms_client = boto3.client('kms')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    
    for record in event['Records']:
        #pull the body out & json load it
        jsonmaybe=(record["body"])
        jsonmaybe=json.loads(jsonmaybe)
        
        ##Buscar object_key e nome do Bucket através do evento
        bucket_name = jsonmaybe["Records"][0]["s3"]["bucket"]["name"]
        key=jsonmaybe["Records"][0]["s3"]["object"]["key"]

    
        objetoCriptografado = s3_client.get_object(Bucket=bucket_name, Key=key)["Body"].read()

        #Decriptografando 
        objetoDecriptografado = kms_client.decrypt(CiphertextBlob=objetoCriptografado)['Plaintext'].decode('utf-8')
    
    
        #Buscando ARN no SNS
        SnsArnEncrypted = os.environ['SNS_ARN']
        SnsArnDecrypted = kms_client.decrypt(
        CiphertextBlob=b64decode(SnsArnEncrypted),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
        )['Plaintext'].decode('utf-8')
    
    
        #Publicando no Tópico SNS
        body = objetoDecriptografado
        response = sns_client.publish(
            TargetArn=SnsArnDecrypted,
            Message=json.dumps({'default': json.dumps(body),
                            'sms': '',
                            'email': body}),
            Subject='Conteúdo Decriptografado',
            MessageStructure='json'
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Email enviado com sucesso!')
    }
