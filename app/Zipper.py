import os
import zipfile
from os.path import basename
from zipfile import ZipFile


class Zipper:
    @staticmethod
    def zip_directory(sourceDirectory, target):
        with ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as zipObj:
            for folderName, subfolders, filenames in os.walk(sourceDirectory):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, basename(filePath))
