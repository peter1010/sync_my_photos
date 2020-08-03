# sync_my_photos
Collect from all my devices and synchronise my server collection of photos with Flickr

# User Requirements

* R001 - Maintain a local (home server) store of all photos
* R002 - Backup home server to online service, to avoid los of photos
* R003 - Allow photos to be seen remotely via phone or web-browser
* R004 - Minimise load to internet connection especially during the day

# Proposed Solution
* Use Flickr as the online service (covers R002 & R003)
* Use a scheduler uploader to flickr once a day at 2AM - covers R004
* Use rsync to copy files from phones /camera to home server - covers R001

# System breakdown
* home service has the intelligence - written in python
* SimpleSSHD running on each phone
* Cannon powershot?? TBD

# SimpleSSHD

http://www.galexander.org/software/simplesshd/

Download and install api. Set up public/private key as per instructions

Things to note IP address, port and location of photos on the phone.
For my phone, photos are located at /storage/emulated/0/DCIM/Camera

# Flickr

To access Flickr you need to create API key and secret, details found when
logging into flickr.



