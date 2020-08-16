import os
import logging
import subprocess
import datetime

#from . import photo

class Android_ssh:

    def __init__(self, ip_addr, port, path):
        self.ip_addr = ip_addr
        self.port = port
        self.path = path
  #      self.photos = self.get_photo_list()

    def get_photo_list(self):
        photos = []
        args = ["ssh", "-p", str(self.port), self.ip_addr, "ls", "-o", self.path]
        listing = subprocess.check_output(args)
        # -rw-rw---- 1 root 40526683 2020-07-15 10:27 VID_20200715_102710053.mp4
        for line in listing.splitlines():
            tokens = line.split(maxsplit=7)
            try:
                size, date, time, name = tokens[3:]
            except ValueError:
                continue
            size = int(size)
            pathname = name.decode("utf-8")
            if not pathname.lower().endswith(".jpg"):
                continue
            photos.append((pathname, size))
        return photos

