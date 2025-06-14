import boto3
import os

s3 = boto3.client('s3')
translate = boto3.client('translate')

# Optional: Set default output bucket, can be overridden with environment variable
DEFAULT_OUTPUT_BUCKET = 'translate-capstone-response'

def lambda_handler(event, context):
    print("Received event:", event)

    try:
        # Extract bucket name and object key from S3 event
        record = event['Records'][0]
        input_bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        print(f"Input Bucket: {input_bucket}, Key: {key}")

        # Download original file
        response = s3.get_object(Bucket=input_bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')

        # Translate text
        translation_result = translate.translate_text(
            Text=file_content,
            SourceLanguageCode='en',
            TargetLanguageCode='fr'
        )
        translated_text = translation_result['TranslatedText']

        print("Translation complete")

        # Determine output bucket (env variable or default)
        output_bucket = os.environ.get('OUTPUT_BUCKET', DEFAULT_OUTPUT_BUCKET)
        output_key = f"translated/{key}"

        # Upload translated result to output bucket
        s3.put_object(Bucket=output_bucket, Key=output_key, Body=translated_text.encode('utf-8'))

        print(f"Uploaded to {output_bucket}/{output_key}")

        return {
            'statusCode': 200,
            'body': f"Translation uploaded to {output_bucket}/{output_key}"
        }

    except Exception as e:
        print("Error:", str(e))
        raise
