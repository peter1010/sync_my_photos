import os
import logging
import configparser
import sqlite3

from .local_db import LocalDb

def load_config():
    """Load from the configuration file "/etc/sync_my_photos.ini" configuration
    variables."""
    cameras = []
    cloud_cfg = None
    local_cfg = None
    config = configparser.ConfigParser()
    config.read(os.path.join("/etc", "sync_my_photos.ini"))
    sections = config.sections()
    for name in sections:
        if name.startswith("Camera"):
            cameras.append(config[name])
        if name.startswith("Cloud"):
            cloud_cfg = config["Cloud"]
        if name.startswith("Local"):
            local_cfg = config["Local"]
    return cameras, cloud_cfg, local_cfg



def upload_from_android(config, local_db):
    from . import android_ssh
    ip_addr = config["ip"]
    port = int(config["port"])
    path = config["path"]
    name = config["name"]
    src = android_ssh.Android_ssh(ip_addr, port, path)
    photos = src.get_photo_list()
    for pathname, size in photos:
        entry = local_db.get_info(name, pathname, size)
        if not entry.already_uploaded:
            src.copy_photo(pathname)

#    print(photos)

def upload(config, local_db):
    typ = config["type"]
    if typ == "android":
        upload_from_android(config, local_db)


def run():
    log = logging.getLogger()
    ch = logging.StreamHandler()
    log.addHandler(ch)

    camera_cfgs, cloud_cfg, local_cfg = load_config()
    local_db = LocalDb(local_cfg)

    for cfg in camera_cfgs:
        upload(cfg, local_db)


#    if args.debug:
#        print("Debug enabled")
#        log.setLevel(logging.DEBUG)

    print("Syncing...")
#    src = android_ssh.Android_ssh()
#    photos = src.get_photo_list()
#    print(photos)

    
run()
