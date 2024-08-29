# Blogs and ARticles Display Server 

The **B**logs and **AR**ticles **D**isplay **S**erver (**BARDS**) is a python server for hosting a customisable website used to create, edit and display articles. It is intended to be used to write about my personal projects and programming experience (these articles will not be included).


> [!IMPORTANT]
> This repositry is intended to be used with Amazon Web Services. To run the repository on a local server, either use main.py (not reccommended) or install and setup a new framework.

## Getting Started

1. Clone the repository to a local destination using git and enter the repository.

		git clone https://github.com/GalacticKittenSS/Blog

1. Install python module dependencies using pip.

		pip install -r bards/requirements.txt

1. Create a .env file, and add: 

		EDITOR_USERNAME = '[your username]'
		EDITOR_PASSWORD = '[your password]'

> [!WARNING]
> Do not use an existing password, as minimal security efforts are in place.


1. Run the editor

		python editor.py

1. Start creating articles by opening [localhost:3000](http://localhost:3000) in a browser and login using the username and password set in the .env file

## Publishing
Once you have finished creating articles, you can...

- Run a preview of the live website:

		python main.py

> [!CAUTION]
> Both [main.py](main.py) and [editor.py](editor.py) should only be used for development purposes, due to the use of the [http.server](https://docs.python.org/3/library/http.server.html) module.

> [!WARNING]
> http.server is not recommended for production. It only implements basic security checks. [docs.python.org/3/library/http.sever](https://docs.python.org/3/library/http.server.html)

- Publish to [Amazon Web Services](https://aws.amazon.com):

	1. Install and setup [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html)

	1. Create an S3 Bucket in AWS and set s3_bucket in [aws-lambda/samconfig.toml](aws-lambda/samconfig.toml)
				
			[default.deploy.parameters]
			s3_bucket = "[Your AWS Bucket Name]"

	1. Create an [AWS IAM User](https://us-east-1.console.aws.amazon.com/iam/home#/users) with [AmazonS3FullAccess](https://us-east-1.console.aws.amazon.com/iam/home#/policies/details/arn%3Aaws%3Aiam%3A%3Aaws%3Apolicy%2FAmazonS3FullAccess?section=permissions) policies

	1. Open the .env file and add:

			AWS_ID = '[Your AWS IAM User ID]'
			AWS_SECRET = '[Your AWS IAM User Secret]'
			AWS_BUCKET = '[Your AWS Bucket Name]/BARDS'
	
	1. Upload to AWS using AWS SAM:

			aws-lambda/deploy

	1. Open your browser to the URL listed under the key 'BardsFunctionUrlEndpoint'.


