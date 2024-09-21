@echo off

:: Start from aws-lambda directory (no matter which starting directory)
cd /D "%~dp0"

:: Load .env with AWS_ID, AWS_SECRET and AWS_BUCKET
for /F "delims==,' tokens=1,3 eol=#" %%i in (../.env) do set %%i=%%j

echo Copying Appropriate Files and Folders to AWS S3
aws s3 cp ../Articles s3://%AWS_BUCKET %/Articles/ --recursive
aws s3 cp ../Assets/images s3://%AWS_BUCKET %/Assets/images --recursive
aws s3 cp ../Assets/pages/templates s3://%AWS_BUCKET %/Assets/pages/templates --recursive
aws s3 cp ../Assets/scripts/main.js s3://%AWS_BUCKET %/Assets/scripts/main.js
aws s3 cp ../Assets/styles/mainstyle.css s3://%AWS_BUCKET %/Assets/styles/mainstyle.css
aws s3 cp ../Assets/styles/light.css s3://%AWS_BUCKET %/Assets/styles/light.css
aws s3 cp ../Assets/styles/dark.css s3://%AWS_BUCKET %/Assets/styles/dark.css

echo Building and Deploying to AWS
:: This has to be on one line, or no commands will execute after sam build
sam build & sam deploy --parameter-overrides AWSID=%AWS_ID % AWSSecret=%AWS_SECRET % AWSBucket=%AWS_BUCKET %
