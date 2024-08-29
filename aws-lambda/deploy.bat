@echo off

:: Start from aws-lambda directory (no matter which starting directory)
cd /D "%~dp0"

:: Load .env with AWS_ID, AWS_SECRET and AWS_BUCKET
for /F "delims==,' tokens=1,3 eol=#" %%i in (../.env) do set %%i=%%j

echo Building and Deploying to AWS
:: This has to be on one line, or no commands will execute after sam build
sam build & sam deploy --parameter-overrides AWSID=%AWS_ID % AWSSecret=%AWS_SECRET % AWSBucket=%AWS_BUCKET %
