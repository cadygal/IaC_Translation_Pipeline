import json
import boto3
import os

s3 = boto3.client('s3')
translate = boto3.client('translate')

def lambda_handler(event, context):
    print("Event Received:")
    print(json.dumps(event))

    try:
        input_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        response = s3.get_object(Bucket=input_bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        data = json.loads(file_content)

        source = data['source_lang']
        target = data['target_lang']
        text = data['text']

        translated = translate.translate_text(
            Text=text,
            SourceLanguageCode=source,
            TargetLanguageCode=target
        )

        output = {
            "translated_text": translated['TranslatedText'],
            "source_lang": source,
            "target_lang": target
        }

        output_key = key.replace('.json', '_translated.json')
        output_bucket = os.environ['RESPONSE_BUCKET']

        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=json.dumps(output)
        )

        return {
            'statusCode': 200,
            'body': f'Translated file saved as {output_key} in {output_bucket}'
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise
