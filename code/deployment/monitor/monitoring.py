import datetime
import glob
import numpy as np
import os
import schedule
import threading
import time

from azure.storage.blob import BlobProperties, BlobServiceClient, BlobClient, ContainerClient


if 'MAX_FILE_LEN' not in os.environ.keys():
    os.environ['MAX_FILE_LEN'] = '50000'


class InvalidData(Exception):
    pass

# This is from implementation of run_continuously
# https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py#L63


class ModelDataCollector:
    def __init__(self, features, model_name, dstore=None):
        self.buffer = []

        # Construct the connection string if passed a datastore
        if dstore is not None:
            os.environ['DS_CONNECTION_STRING'] = \
                'DefaultEndpointsProtocol=' + dstore.protocol + \
                ';AccountName=' + dstore.account_name + ';AccountKey=' \
                + dstore.account_key + ';EndpointSuffix=' + dstore.endpoint
        print(f"DEBUG: connection string is {os.environ['DS_CONNECTION_STRING']}")
        self.client = BlobServiceClient.from_connection_string(os.getenv('DS_CONNECTION_STRING'))
        self.container = "modeldata"
        self.features = features
        self.model_name = model_name
        self.last_time
        
        interval = 60

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while True:
                    print("DEBUG: thread job run")
                    self.upload_to_blob()
                    time.sleep(interval)
                    
        continuous_thread = ScheduleThread()
        continuous_thread.start()

        #schedule.every(1).minutes.do(self.upload_to_blob)
    
    def collect(self, data):
        if len(data) != len(self.features):
            raise InvalidData(f"Passed in data of length {len(data)} but expected data of length {len(self.features)}")
    
        # Initialize buffer if empty
        if len(self.buffer) == 0:
            print('initializing buffer')
            self.buffer = np.array(data)
            
        # If we are not yet at max file size, keep appending
        elif (len(self.buffer)+len(data) < (int(os.getenv('MAX_FILE_LEN')) - 1)):
            print(f'DEBUG: reached append path, len buffer is {len(self.buffer)}')
            self.buffer = np.row_stack((self.buffer, data))

        # else, write file
        else:
            print(f'DEBUG: reeached write path when len buffer was {len(self.buffer)} len data was {len(data)}')
            self.save_buffer_to_file()

            # Reinitialize buffer with current input sample
            self.buffer = np.array(data)
            print(f'DEBUG: buffer reinitialized {self.buffer}')


    def save_buffer_to_file(self, current_time=datetime.datetime.now()):
        # only write a file if there is something to save
        if len(self.buffer) > 0:
            file_path = current_time.strftime(f"{self.model_name}/%Y/%m/%d/%H/%M/%S")
            os.makedirs(file_path)
            file_name = os.path.join(file_path, 'data.csv')
            print(f'file name is {file_name}')
            print(f'Attempting to save data with len {len(self.buffer)} with features with len {len(self.features)}')

            header = ','.join([str(element) for element in self.features])
            np.savetxt(file_name, self.buffer, delimiter=',', header=header, comments='', fmt=["%s"]*len(self.features))

            # empty buffer
            self.buffer = []
        else:
            return

    def upload_to_blob(self):
        print('DEBUG: upload_to_blob called')
        self.save_buffer_to_file()
        files_to_upload = glob.glob(f'{self.model_name}/*/*/*/*/*/*/*.csv')

        print(f'DEBUG: file_to_upload {files_to_upload}')

        # Don't do anything if there are no new files
        if len(files_to_upload)==0:
            print(f'DEBUG: no files to upload')
            return
        
        # Upload the created files to blob
        for file_name in files_to_upload:
            blob_client = self.client.get_blob_client(container=self.container, blob=file_name.lstrip('/'))
            print("\nUploading to Azure Storage as blob:\n\t" + file_name)
            with open(file_name, "rb") as upload_data:
                blob_client.upload_blob(upload_data)
            
            # remove file from local storage
            os.remove(file_name)
