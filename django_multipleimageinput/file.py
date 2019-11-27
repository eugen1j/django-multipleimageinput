import os
from pathlib import Path
from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from shutil import copyfile


class Storage:
    SUBDIRECTORY_NAME_SIZE = 2

    def __init__(self, directory: str):
        self._directory = directory

    def save(self, name: str, content: Union[bytes, str, InMemoryUploadedFile, TemporaryUploadedFile]) -> str:
        if len(name) <= self.SUBDIRECTORY_NAME_SIZE:
            raise ValueError(f"filename '{name}' is too short")
        subdirectory = name[:self.SUBDIRECTORY_NAME_SIZE]
        directory = Path(self._directory) / subdirectory
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = directory / name

        if content is bytes:
            with open(file_path, 'wb') as file:
                file.write(content)
        elif content is str:
            with open(file_path, 'w') as file:
                file.write(content)
        elif isinstance(content, InMemoryUploadedFile):
            with open(file_path, 'wb') as file:
                for chunk in content.chunks():
                    file.write(chunk)
        elif isinstance(content, TemporaryUploadedFile):
            copyfile(content.temporary_file_path(), file_path)
        else:
            raise TypeError(f"content has invalid type")

        return Path(subdirectory) / name
