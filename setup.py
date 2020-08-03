#!/usr/bin/env python3

import os
from distutils.core import setup
from distutils.command import install


class my_install(install.install):
    def run(self):
        retVal = super().run()
        if self.root is None or not self.root.endswith("dumb"):
            if not os.getenv("DONT_START"):
                from src import service
                service.start_service()
        return retVal


setup(
    name='sync_my_photos',
    version='1.0',
    description="Sync my collection of photos",
    url='https://github.com/peter1010/sync_my_photos',
    author='Peter1010',
    author_email='peter1010@localnet',
    license='GPL',
    package_dir={'sync_my_photos': 'src'},
    packages=['sync_my_photos'],
    data_files=[
        ('/usr/lib/systemd/system',
         ('sync_my_photos.timer', 'sync_my_photos.service'))
    ],
    cmdclass={'install': my_install}
)
