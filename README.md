# dq-generic-virus-scanner

This repo houses a dockerized virus scanning solution which utilizes a ClamAV instance to virus scan
files in a configured directory and output the files to a configured S3 bucket.

## Usage

This repo does not provide a file acquisition functionality. There is an example function `pull_files()` in `app/scripts/file_ingest.py` which simulates the acquisition of files for demonstration purposes. However for production usage you will be required to replace this with an appropriate function to pull files from your desired location.

## Configuration


| Environment Variable | Example        | Description                             | Required |
|----------------------|----------------|-----------------------------------------|----------|
| S3_BUCKET_NAME       | my_bucket      | Bucket to output clean files to         |  Yes     |
| BUCKET_KEY_PREFIX    | my/path        | File prefix used when uploading to S3   |  Yes     |
| S3_ACCESS_KEY_ID     | AK124512A      | Access key id for S3 Bucket             |  Yes     |
| S3_SECRET_ACCESS_KEY | YKJADAS12      | Access key secret for S3 bucket         |  Yes     |
| S3_REGION_NAME       | eu-west-2      | Region the S3 bucket resides in         |  Yes     |
| BASE_URL             | localhost      | Base URL of clamav service              |  No      |
| BASE_PORT            | 8080           | Port used for clamav service            |  No      |
| INPUT_DIR            | /tmp/input     | Dir files will be acquired into         |  No      |
| OUTPUT_DIR           | /tmp/output    | Dir files are placed in before upload   |  No      |
| QUARANTINE_DIR       | /tmp/quarantine| Dir virus files are placed in           |  No      |

## Local development

Given the neccessary environment variables have been set. You can set the application up by:

1. Install dependencies
`pip install -r packages.txt`

2. Starting up a local clamAv instance through docker-compose
`docker-compose up`

3. Starting the process by running
`python scripts/file_ingest.py`

## Deployment

Kube files are provided for deployment including a persistant volume claim
in order to prevent loss of files if moving files from an external location and the pod diess
