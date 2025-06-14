AWS Translation Pipeline (Capstone Project)

Overview

This project demonstrates a serverless language translation pipeline on AWS using:
- AWS S3 (for input/output storage)
- AWS Translate (for language translation)
- AWS Lambda (for backend processing)
- AWS CloudFormation (for Infrastructure as Code)


Setup & Deployment

1. Clone the Repository
   ```bash
   git clone https://github.com/cadygal/IaC_Translation_Pipeline.git
   cd IaC_Translation_Pipeline

Package Lambda Script
Compress-Archive -Path lambda/translator.py -DestinationPath lambda/translator.zip

Upload Lambda Package
aws s3 cp lambda/translator.zip s3://translate-capstone-artifacts/lambda/translator.zip

Deploy CloudFormation Stack
aws cloudformation deploy `
  --template-file templates/main.yaml `
  --stack-name translate-capstone `
  --capabilities CAPABILITY_NAMED_IAM `
  --parameter-overrides `
    LambdaZipS3Bucket=translate-capstone-artifacts `
    LambdaZipS3Key=lambda/translator.zip

JSON Format
Upload input JSON files to the translate-capstone-request bucket in this format:
{
  "source_lang": "en",
  "target_lang": "fr",
  "text": "Hello, how are you?"
}

How Translation Works
Upload a JSON file to the request bucket.
This triggers an S3 event notification.
Lambda function reads the file, translates the text using AWS Translate.
Result is written to the translate-capstone-response bucket.

IAM Permissions
Lambda Role allows:
translate:TranslateText
s3:GetObject, s3:PutObject

CloudWatch logs permissions

IAM Role is defined in the CloudFormation template.

Troubleshooting
Issue: Translated file not appearing in response bucket
Check:

 CloudWatch Logs: Check Lambda logs for errors

 IAM Permissions: Ensure Lambda role has s3:PutObject access to response bucket

 S3 Trigger: Confirm event notification is correctly set on request bucket

 JSON Format: Input must match required structure

 File Encoding: Input file must be UTF-8 encoded

 Lambda Environment: Ensure RESPONSE_BUCKET env variable is configured

