import os
import subprocess
import datetime
import re


class Exif:
    def __init__(self, pathname):
        self.pathname = pathname
        self.load_exif()

    def load_exif(self):
        args = ["exiv2", "-g", "DateTime", self.pathname]
        listing = subprocess.check_output(args)
        # Exif.Image.DateTime  Ascii  20 2003:06:27 12:46:11
        for line in listing.splitlines():
            tokens = line.split()
            Name = tokens[0]
            if not Name.startswith(b"Exif."):
                continue
            Name = Name[5:]
            if tokens[1] != b"Ascii":
                print(self.pathname)
                print(line)
                raise RuntimeError

            Value = b" ".join(tokens[3:])
            self.process_date(Name, Value)
        return self.Year

    def process_date(self, Name, Value):
        # YYYY:MM:DD HH:MM:SS
        # YYYY-MM-DD HH:MM:SS
        # DD/MM/YYYY HH:MM
        m = re.fullmatch(b"(\\d+):(\\d+):(\\d+) (\\d+):(\\d+):(\\d+)", Value)
        if m:
            result = (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6))
        else:
            m = re.fullmatch(b"(\\d+)-(\\d+)-(\\d+) (\\d+):(\\d+):(\\d+)", Value)
            if m:
                result = (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6))
            else:
                m = re.fullmatch(b"(\\d+)/(\\d+)/(\\d+) (\\d+):(\\d+)", Value)
                if m:
                    result = (m.group(3), m.group(2), m.group(1), m.group(4), m.group(5), b"0")

        try:
            self.Year = int(result[0])
            assert self.Year >= 1000 and self.Year <= 9999
            self.Month = int(result[1])
            assert self.Month <= 12
            self.Day = int(result[2])
            assert self.Month <= 31
            self.Hour = int(result[3])
            assert self.Hour <= 23
            self.Minute = int(result[4])
            assert self.Minute <= 59
            self.Second = int(result[5])
            assert self.Second <= 59
        except ValueError:
            print(self.pathname)
            raise


    def GetDatePhotoTaken(self):
        pass
