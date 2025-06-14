import json
import boto3
import os

s3 = boto3.client('s3')
translate = boto3.client('translate')

def lambda_handler(event, context):
    input_bucket = os.environ.get('INPUT_BUCKET')
    output_bucket = os.environ.get('OUTPUT_BUCKET')

    # Parse file info from S3 event
    key = event['Records'][0]['s3']['object']['key']
    response = s3.get_object(Bucket=input_bucket, Key=key)
    data = json.loads(response['Body'].read())

    source_lang = data['source_language']
    target_lang = data['target_language']
    text = data['text']

    translated = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )

    result = {
        'original': text,
        'translated': translated['TranslatedText'],
        'source_language': source_lang,
        'target_language': target_lang
    }

    output_key = key.replace(".json", "_translated.json")
    s3.put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=json.dumps(result)
    )

    return {"status": "done", "output_key": output_key}
