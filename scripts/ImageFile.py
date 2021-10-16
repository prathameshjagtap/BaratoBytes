from PIL import Image
from os import path
import imghdr

class ImageFile:

    def __init__(self, path):
        self.path = path
        self.image_type = imghdr.what(path)
        self.suffix = '_compressed'

        if self.image_type is not None:
            self.image = Image.open(path)
        else:
            self.image = None

    def compress(self):
        file_name = path.splitext(self.path)
        compressed_path = file_name[0] + self.suffix + file_name[1]

        if self.image is None:
            return None
        else:
            self.image = self.image.resize((int(self.image.size[0]/2), int(self.image.size[1]/2)), Image.ANTIALIAS)
            self.image.save(compressed_path, optimize=True, quality=30)
            return compressed_path
