from ftplib import FTP
from threading import Thread, Event
from queue import Queue, Empty
from io import BytesIO


class FTPDownloader(object):
    def __init__(self, host, user, password, timeout=0.01):
        self.ftp = FTP(host)
        self.ftp.login(user, password)
        self.timeout = timeout

    def getBytes(self, filename):
        print("getBytes")
        self.ftp.retrbinary("RETR {}".format(filename), self.bytes.put)
        self.bytes.join()   # wait for all blocks in the queue to be marked as processed
        self.finished.set()  # mark streaming as finished

    def sendBytes(self):
        while not self.finished.is_set():
            try:
                yield self.bytes.get(timeout=self.timeout)
                self.bytes.task_done()
            except Empty:
                self.finished.wait(self.timeout)
        self.worker.join()

    def download(self, filename):
        self.bytes = Queue()
        self.finished = Event()
        self.worker = Thread(target=self.getBytes, args=(filename,))
        self.worker.start()
        return self.sendBytes()
