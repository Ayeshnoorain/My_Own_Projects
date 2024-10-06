import json
import boto3
import datetime
import os
from openai import OpenAI

# Initialize the S3 client
s3_client = boto3.client('s3')

# Get the S3 bucket name and OpenAI API key from environment variables
bucket_name = os.getenv('S3_BUCKET_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=openai_api_key)

def lambda_handler(event, context):
    # Log the incoming event for debugging purposes
    print("Event received by Lambda:", json.dumps(event))
    
    # Extract user input from query string parameters
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        user_input = event['queryStringParameters'].get('user_input', 'No input provided')
    else:
        user_input = 'No input provided'
    
    # System message setup for Chat Completion
    system_message = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI Customer Support."
                }
            ]
        }
    ]
    
    # User input message for the Chat Completion
    user_message = [
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    # Call OpenAI GPT API to get the AI response
    try:
        # Call OpenAI API using the new client method
        response = client.chat.completions.with_raw_response.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=system_message + user_message,
            max_tokens=100,  # Adjust the number of tokens as necessary
            top_p=0.01  # You can adjust top_p or other parameters as needed
        )

        # Extract AI response from the 'choices' field
        ai_response = response.http_response.json()["choices"][0]["message"]["content"].strip()
        
        # Optionally log or return the API usage and response time
        usage_info = response.http_response.json().get("usage", {})
        time_taken = response.elapsed.total_seconds()

    except Exception as e:
        # Handle errors by capturing the exception
        ai_response = f"Error generating response: {str(e)}"
        usage_info = {}
        time_taken = 0
    
    # Prepare the data to be stored in S3
    response_data = {
        "user_input": user_input,
        "ai_response": ai_response,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "usage_info": usage_info,
        "time_taken": f"{time_taken:.2f}s"
    }
    
    # Create a unique filename using the current timestamp
    filename = f"response_{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.json"
    
    # Upload the JSON object to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=json.dumps(response_data),
        ContentType='application/json'
    )
    
    # Return the AI response to the user
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Response saved successfully!",
            "user_input": user_input,
            "ai_response": ai_response,
            "filename": filename,
            "usage_info": usage_info,
            "time_taken": f"{time_taken:.2f}s"
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }
