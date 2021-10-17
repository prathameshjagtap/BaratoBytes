from os import remove
from os import walk
from os.path import join
from UserAccount import UserAccount
from ImageFile import ImageFile

import logging
import boto3
from botocore.exceptions import ClientError


class FileSyncClient:

    def __init__(self, user_account: UserAccount):
        self.user_account = user_account
        self.s3_client = boto3.client('s3')
        self.whole_files_s3dir = 'wholefiles'
        self.compressed_files_s3dir = 'compressedfiles'

    def get_new_local_files(self, existing_file_list, dir=None):
        if dir == None:
            dir = self.user_account.local_directory
        dir_files_list = []
        for (dirpath, dirnames, filenames) in walk(dir):
            for filename in filenames:
                dir_files_list.append(join(dirpath, filename))
            for newdir in dirnames:
                dir_files_list.extend(self.get_new_local_files(existing_file_list, join(dirpath, newdir)))
            break
        existing_files_absolute_path = []
        existing_files_absolute_path.extend(join(self.user_account.local_directory, x) for x in existing_file_list)
        new_local_files = [item for item in dir_files_list if item not in existing_files_absolute_path]
        return new_local_files

    def upload_whole_files(self, file_list):
        for file_name in file_list:
            file_key_name = self.whole_files_s3dir + file_name.replace(self.user_account.local_directory, '')
            try:
                self.s3_client.upload_file(file_name, self.user_account.bucket_name, file_key_name)
                logging.info('file %s uploaded at %s', file_name, file_key_name)
            except ClientError as e:
                logging.error(e)

    def upload_compressed_files(self, file_list):
        for file_name in file_list:
            file_key_name = self.compressed_files_s3dir + file_name.replace(self.user_account.local_directory, '')
            try:
                image_file = ImageFile(file_name)
                if image_file.image_type is not None:
                    compressed_file_path = image_file.compress()
                    self.s3_client.upload_file(compressed_file_path, self.user_account.bucket_name, file_key_name)
                    remove(compressed_file_path)
                    logging.info('file %s uploaded at %s', compressed_file_path, file_key_name)
                else:
                    logging.info('file %s skipped for compression', file_name)
            except ClientError as e:
                logging.error(e)

    def get_existing_whole_files(self):
        existing_whole_files = []
        existing_whole_files.extend(key['Key'].replace(self.whole_files_s3dir + '/', '')
                                    for key in self.s3_client.list_objects(Bucket=self.user_account.bucket_name,
                                                                           Prefix=self.whole_files_s3dir)['Contents'])
        existing_whole_files.remove('')
        return existing_whole_files
