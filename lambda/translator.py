import json, os, boto3, traceback
s3 = boto3.client("s3")
translate = boto3.client("translate")

def lambda_handler(event, context):
    # 🔎 1. Log the raw event so we always know what we got
    print("Event Received:")
    print(json.dumps(event, indent=2))

    try:
        # 💡 2. Extract bucket/key from REAL S3 event
        records = event.get("Records", [])
        if not records:
            raise ValueError("No S3 records in event")

        input_bucket = records[0]["s3"]["bucket"]["name"]
        key          = records[0]["s3"]["object"]["key"]

        # 🗄️ 3. Download the file
        obj = s3.get_object(Bucket=input_bucket, Key=key)
        data = json.loads(obj["Body"].read())

        src  = data["source_lang"]
        dst  = data["target_lang"]
        text = data["text"]

        # 🌐 4. Translate
        out  = translate.translate_text(Text=text,
                                        SourceLanguageCode=src,
                                        TargetLanguageCode=dst)

        result = {
            "original_text": text,
            "translated_text": out["TranslatedText"],
            "source_lang": src,
            "target_lang": dst
        }

        # 📨 5. Write to response bucket
        out_bucket = os.environ["RESPONSE_BUCKET"]
        out_key    = key.replace(".json", "_translated.json")

        s3.put_object(Bucket=out_bucket,
                      Key=out_key,
                      Body=json.dumps(result, indent=2).encode())

        return {"statusCode": 200,
                "body": f"Saved {out_bucket}/{out_key}"}

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        raise
