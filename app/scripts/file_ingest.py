#!/usr/bin/python3

import os
import sys
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import urllib.request
import boto3
import requests

from virus_scanner import VirusScanner

BUCKET_NAME             = os.environ['S3_BUCKET_NAME']
BUCKET_KEY_PREFIX       = os.environ['S3_KEY_PREFIX']
S3_ACCESS_KEY_ID        = os.environ['S3_ACCESS_KEY_ID']
S3_SECRET_ACCESS_KEY    = os.environ['S3_SECRET_ACCESS_KEY']
S3_REGION_NAME          = os.environ['S3_REGION_NAME']
BASE_URL                = os.environ.get('CLAMAV_URL', 'localhost')
BASE_PORT               = os.environ.get('CLAMAV_PORT', '8080')
INPUT_DIR               = os.environ.get('INPUT_DIR', '/tmp/input')
OUTPUT_DIR              = os.environ.get('OUTPUT_DIR', '/tmp/output')
QUARANTINE_DIR          = os.environ.get('QUARANTINE_DIR', '/tmp/quarantine')


def pull_files():
    """Temp function to simulate pulling of files
    """
    for i in range(10):
        with open(f'/tmp/test/file{i}', 'a') as f:
            f.write('Hello world')

def move_file_s3(file_location):
    try:
        today = datetime.datetime.now()
        file_name = file_location.split('/')[-1]
        boto_s3_session = boto3.Session(
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
            region_name=S3_REGION_NAME
        )
        s3_conn = boto_s3_session.client("s3")
        s3_conn.upload_file(
            file_location,
            BUCKET_NAME,
            f'{BUCKET_KEY_PREFIX}/{today.year}/{today.month}/{today.day}/{file_name}'
        )
        print(f'Uploaded: {file_name}')
    except Exception as err:
        print(f'Failed to upload: {file_name}')
        print(err)

def main():
    pull_files()

    scanner = VirusScanner(INPUT_DIR, OUTPUT_DIR, QUARANTINE_DIR, BASE_URL, BASE_PORT)
    scanner.scan()

    for clean_file in os.listdir(OUTPUT_DIR):
        move_file_s3(f'{OUTPUT_DIR}/{clean_file}')


if __name__ == '__main__':
    main()