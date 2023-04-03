import json
import boto3

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    

    queue_type = event['type']
    
   
    if queue_type == 'CONNECT':
        queue_url = 'https://sqs.us-east-1.amazonaws.com/401550115657/Connect'
    elif queue_type == 'SUBSCRIBE':
        queue_url = 'https://sqs.us-east-1.amazonaws.com/401550115657/Subscribe'
    elif queue_type == 'PUBLISH':
        queue_url = 'https://sqs.us-east-1.amazonaws.com/401550115657/Publish'

    
   
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=0
    )
    
   
    if 'Messages' in response:
        message = response['Messages'][0]
        message_contents = json.loads(message['Body'])
        
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
        
        if queue_type == 'CONNECT':
            response_body = {
                'type': 'CONNACK',
                'returnCode': 0,
                'username': message_contents['username'],
                'password': message_contents['password']
            }
        elif queue_type == 'SUBSCRIBE':
            response_body = {
                'type': 'SUBACK',
                'returnCode': 0
            }
        elif queue_type == 'PUBLISH':
            response_body = {
                'type': 'PUBACK',
                'returnCode': 0,
                'payload': message_contents['payload']
            }
        
        return json.loads(json.dumps(response_body))
    else:
        
     

            if queue_type == 'CONNECT':
                return json.loads(json.dumps({'type': 'CONNACK', 'returnCode': 0, 'username': '', 'password': ''}))
        
            elif queue_type == 'SUBSCRIBE':
                return json.loads( json.dumps({'type': 'SUBACK', 'returnCode': 0}))
    
            elif queue_type == 'PUBLISH':
                return  json.loads(json.dumps({'type': 'PUBACK','returnCode': 0,'payload': {'key': 'location', 'value': '44.637437,-63.587206'}}))
        
        
