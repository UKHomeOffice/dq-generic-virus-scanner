#!/usr/bin/python3

import os
import sys
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import urllib.request
import boto3
import requests

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


class VirusScanner:
    """Class for interacting with a ClamAV vir scanning service"""
    def __init__(self, input_dir, output_dir, quarantine_dir, scanner_host, scanner_port):
      self.input_dir = input_dir
      self.output_dir = output_dir
      self.quarantine_dir = quarantine_dir
      self.scanner_host = scanner_host
      self.scanner_port = scanner_port
    
    def scan(self):
        """Virus scan each file in the configured input directory
            Move files found to contain a virus to the quarantine directory
            Move clean files to the output directory

        Returns: 
            None
        """
        print('Starting virus scan')
        for file_name in os.listdir(self.input_dir):
            print(f'Virus scanning {file_name}')
            with open(f'{self.input_dir}/{file_name}', 'rb') as file_contents:
                response = requests.post('http://' + self.scanner_host + ':' + self.scanner_port + '/scan', files={'file': file_contents}, data={'name': file_name})
                if not 'Everything ok : true' in response.text:
                    print(f'Virus scan FAIL: {file_name} is dangerous! Moving to quarantine')
                    self._move_file(file_name, self.quarantine_dir)
                    continue
                else:
                    print(f'Virus scan OK: {file_name}')
                    self._move_file(file_name, self.output_dir)
        print('Scan complete')

    def _create_dir(self, dir_location):
        if not os.path.isdir(dir_location):
            print('Output dir does not exist, creating')
            os.mkdir(dir_location)

    def _move_file(self, file_name, output_dir):
        self._create_dir(output_dir)
        os.rename(os.path.join(self.input_dir, file_name), os.path.join(output_dir, file_name))

def pull_files():
    """Temp function to simulate pulling of files
    """
    for i in range(10):
        if not os.path.isdir(INPUT_DIR):
            os.mkdir(INPUT_DIR)
        with open(f'{INPUT_DIR}/file{i}', 'a') as f:
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