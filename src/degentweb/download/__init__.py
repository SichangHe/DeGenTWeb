import os
from concurrent import futures
from dataclasses import dataclass
from typing import Iterable

import requests


@dataclass
class FileNUrl:
    """File path and URL."""

    file: str
    url: str

    def download(self):
        """Download the file from the URL if it is missing."""
        if os.path.exists(self.file):
            return
        response = requests.get(self.url)
        response.raise_for_status()
        dirname = os.path.dirname(self.file)
        if dirname != "":
            os.makedirs(dirname, exist_ok=True)
        with open(self.file, "wb") as f:
            assert f.write(response.content) == len(response.content), response
        print(f"Downloaded {self.url} -> {self.file}.")


def download_all(file_n_urls: Iterable[FileNUrl]):
    with futures.ThreadPoolExecutor() as executor:
        for _ in executor.map(FileNUrl.download, file_n_urls):
            pass
