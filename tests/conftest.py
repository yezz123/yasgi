import sys
from multiprocessing import Process
from os import path
from time import sleep

import pytest
import uvicorn

sys.path.insert(0, path.realpath(__file__).replace("/tests/conftest.py", "/"))


class Server:
    def __init__(self, app, port=3000):
        self.proc = Process(
            target=self.wrapper, args=(app, port), kwargs={}, daemon=True
        )
        self.proc.start()
        sleep(0.2)

    def stop(self):
        self.proc.terminate()
        sleep(0.1)

    @staticmethod
    def wrapper(app, port):
        uvicorn.run(app(), host="127.0.0.1", port=port, log_level="info")
