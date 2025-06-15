import os
import tempfile
from functools import cached_property
from urllib.parse import urlencode

import requests
from utils import Hash, Log

log = Log("CabinetWebPage")


class CabinetWebPage:
    BASE_URL = "https://www.cabinetoffice.gov.lk/cab/index.php"

    def __init__(self, **params):
        self.params = params

    @cached_property
    def url(self):
        return f"{self.BASE_URL}?{urlencode(self.params)}"

    @cached_property
    def hash(self):
        return Hash.md5(self.url)

    @cached_property
    def __content_hot__(self):

        response = requests.get(self.url)
        response.raise_for_status()
        return response.text

    @cached_property
    def __temp_htmp_file_path__(self):
        return os.path.join(tempfile.gettempdir(), f"{self.hash}")

    @cached_property
    def content(self):
        if not os.path.exists(self.__temp_htmp_file_path__):
            content = self.__content_hot__
            with open(
                self.__temp_htmp_file_path__, "w", encoding="utf-8"
            ) as file:
                file.write(content)
                n_content = len(content.encode("utf-8"))
                log.info(
                    f"Downloaded {
                        self.url} to {
                        self.__temp_htmp_file_path__} ({
                        n_content:,}B)"
                )

        else:
            with open(
                self.__temp_htmp_file_path__, "r", encoding="utf-8"
            ) as file:
                content = file.read()
        return content
