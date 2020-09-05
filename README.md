# ahn_downloader
Tool for downloading Algemeen Hoogtebestand Nederland v3 (AHN3).

## ahn_downloader.py

Python script with ahn downloader class. You can set
* map sheet "kaartbladnummer"
* resolution ('5' or '05')
* type_code ('dsm', 'dtm', 'laz')

The download() function downloads the file to the specified directory, which should already exist.

### Map sheets
You can find the map sheets on this page:
[https://downloads.pdok.nl/ahn3-downloadpage/](https://downloads.pdok.nl/ahn3-downloadpage/)

And in this WFS:
https://geodata.nationaalgeoregister.nl/ahn3/wfs
ahn3:ahn3_bladindex

### Example script
```
from ahn_downloader import AhnDownloader

ad = AhnDownloader('45cn2', resolution='5')
ad.download('/home/raymond/tmp')
```
