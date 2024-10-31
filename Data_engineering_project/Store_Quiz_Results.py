import json
import boto3
import uuid

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Parse the incoming request body
    body = json.loads(event['body'])
    email = body.get('email')
    score = body.get('score')

    if not email or score is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Email and score are required'})
        }

    # Generate a unique file name
    file_name = f"{uuid.uuid4()}.json"

    # Prepare the data
    quiz_result = {
        'email': email,
        'score': score,
        'timestamp': context.aws_request_id  # Unique ID for tracking the request
    }

    # Store the results in S3
    try:
        s3.put_object(
            Bucket='quiz-results-bucket',  # Replace with your actual bucket name
            Key=f"quiz-results/{file_name}",
            Body=json.dumps(quiz_result),
            ContentType='application/json'
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Quiz result stored successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
