import os
import requests

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