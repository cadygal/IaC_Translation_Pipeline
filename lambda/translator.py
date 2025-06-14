import json
import boto3

s3 = boto3.client('s3')
translate = boto3.client('translate')

def lambda_handler(event, context):
    print("EVENT RECEIVED:", json.dumps(event))

    try:
        input_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print(f"Bucket: {input_bucket}")
        print(f"Key: {key}")

        response = s3.get_object(Bucket=input_bucket, Key=key)
        text = response['Body'].read().decode('utf-8')
        
        result = translate.translate_text(
            Text=text,
            SourceLanguageCode='en',
            TargetLanguageCode='fr'
        )

        output_key = key.replace(".json", "-fr.json")

        s3.put_object(
            Bucket=input_bucket.replace("request", "response"),
            Key=output_key,
            Body=result['TranslatedText']
        )

        return {
            'statusCode': 200,
            'body': 'Translation successful'
        }

    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise
