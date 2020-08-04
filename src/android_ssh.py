import os
import logging
import subprocess
import datetime

from . import photo

class Android_ssh:

    CAMERA_PATH = "/storage/emulated/0/DCIM/Camera"
    PORT = 2222

    def __init__(self, ip_addr = "192.168.1.53"):
        self.ip_addr = ip_addr
        self.photos = self.get_photo_list()

    def get_photo_list(self):
        photos = []
        args = ["ssh", "-p", str(self.PORT), self.ip_addr, "ls", "-o", self.CAMERA_PATH]
        listing = subprocess.check_output(args)
        # -rw-rw---- 1 root 40526683 2020-07-15 10:27 VID_20200715_102710053.mp4
        for line in listing.splitlines():
            tokens = line.split(maxsplit=7)
            try:
                size, date, time, name = tokens[3:]
            except ValueError:
                continue
            size = int(size)
            mtime = date + b' ' + time
            mtime = datetime.datetime.strptime(mtime.decode("utf-8"), "%Y-%m-%d %H:%M")
            name = name.decode("utf-8")
            if not name.lower().endswith(".jpg"):
                continue
            photos.append(photo.Photo(size, mtime, name))
            return photos

