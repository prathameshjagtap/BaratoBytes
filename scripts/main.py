from UserAccount import UserAccount
from FileSync import FileSyncClient
# from ImageFile import ImageFile

user = UserAccount("prathamj", "prathameshjagtap-datafiles", "/Users/prathameshjagtap/PycharmProjects/BaratoBytes/data")
f = FileSyncClient(user)

existing_whole_files = f.get_existing_whole_files()

new_local_files = f.get_new_local_files(existing_whole_files)

f.upload_whole_files(new_local_files)
f.upload_compressed_files(new_local_files)

# i = ImageFile("/Users/prathameshjagtap/PycharmProjects/BaratoBytes/data" + '/test')
# i.compress()