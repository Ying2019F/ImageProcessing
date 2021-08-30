import numpy as np

class image(object):
    """
    Image parameters:
    image_array image matirx
    timestamp
    store_name
    camera_id
    barcode
    """
    def __init__(self, image_array, image_id, timestamp, store_name, camera_id, barcode):
        self.image_array = image_array
        self.image_id = image_id
        self.timestamp = timestamp
        self.store_name = store_name
        self.camera_ID = camera_id
        self.barcode = barcode


class TrieNode(object):
    def __init__(self):
        self.counter = 0
        self.children = {}
        self.content = {}


class StorageSystem(object):
    def __init__(self, batch_size):
        self.__root = TrieNode()
        self.batch_size = batch_size

    def saveImages(self, images, file_path):
        """
        :type images: list of image
        :type file_path: str
        :return: void
        """
        current = self.__put(file_path)
        length = len(images)
        remaining = current.counter - self.batch_size
        if length <= remaining:
            for i in range(length):
                current.content[images[i].image_id] = images[i]
                current.counter += 1
        else:
            num = np.ceiling((length - remaining)/self.batch_size)
            for i in range(remaining):
                current.content[images[i].image_id] = images[i]
                current.counter += 1

            for n in range(num):
                current = current.children[str(n)]
                start = n * self.batch_size + remaining
                end = (n+1) * self.batch_size + remaining
                if end < length:
                    for im in images[start:end+1]:
                        current.content[im.image_id] = im
                        current.counter += 1
                else:
                    for im in images[start:length]:
                        current.content[im.image_id] = im
                        current.counter += 1

    def readImages(self, file_path):
        """

        :type file_path: string
        :return: dict of images
        """
        return self.__get(file_path).content

    def __put(self, file_path):
        current = self.__root
        for string in self.__split(file_path, '/'):
            if string not in current.children:
                current.childern[string] = TrieNode()
            current = current.children[string]
        return current

    def __get(self, file_path):
        current = self.__root
        for string in self.__split(file_path, '/'):
            current = current.childern[string]
        return current

    def __split(self, file_path, delimiter):
        if file_path == "/":
            return []
        return file_path.split('/')[1:]


#  Usage
#  obj = StorageSystem()
#  obj.saveImages(list of image, file_path)
#  dict = obj.readImages(file_path)

