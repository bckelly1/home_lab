import argparse
import os
import requests
import shutil
import time
import uuid

# This script calls the HP Printer and triggers a scan job. The scanner then sends a completed PDF back to the script.
# This is intended to be called from within Home Assistant (Python-based). It takes the scanned PDF and sends it to both Paperless and the NAS backup
# After it copies the files it then cleans up the file

IMAGE_SCAN_DIR = os.environ.get('IMAGE_DIR', './')
DOCUMENT_SCAN_DIR = os.environ.get('DOCUMENT_DIR', './')
PAPERLESS_SCAN_DIR = os.environ.get('PAPERLESS_DIR', './')


def image_backup(name, get_response):
    f = open(name, "wb")
    f.write(get_response.content)

    shutil.copy(name, IMAGE_SCAN_DIR)
    shutil.copy(name, PAPERLESS_SCAN_DIR)


def document_backup(name, get_response):
    f = open(name, "wb")
    f.write(get_response.content)

    shutil.copy(name, DOCUMENT_SCAN_DIR)
    shutil.copy(name, PAPERLESS_SCAN_DIR)


parser = argparse.ArgumentParser("scanner_runner")
parser.add_argument("scan_type", help="What kind of scan will it be? pdf, Jpeg", type=str)
args = parser.parse_args()

scan_type = args.scan_type.lower()

if scan_type == 'pdf':
    print('Running a document scan..')
    post_body = '<scan:ScanJob xmlns:scan="http://www.hp.com/schemas/imaging/con/cnx/scan/2008/08/19" xmlns:dd="http://www.hp.com/schemas/imaging/con/dictionaries/1.0/" xmlns:fw="http://www.hp.com/schemas/imaging/con/firewall/2011/01/05"><scan:XResolution>300</scan:XResolution><scan:YResolution>300</scan:YResolution><scan:XStart>0</scan:XStart><scan:YStart>0</scan:YStart><scan:Width>2550</scan:Width><scan:Height>3300</scan:Height><scan:Format>Pdf</scan:Format><scan:CompressionQFactor>0</scan:CompressionQFactor><scan:ColorSpace>Color</scan:ColorSpace><scan:BitDepth>8</scan:BitDepth><scan:InputSource>Platen</scan:InputSource><scan:GrayRendering>NTSC</scan:GrayRendering><scan:ToneMap><scan:Gamma>1000</scan:Gamma><scan:Brightness>1000</scan:Brightness><scan:Contrast>1000</scan:Contrast><scan:Highlite>179</scan:Highlite><scan:Shadow>25</scan:Shadow></scan:ToneMap><scan:ContentType>Document</scan:ContentType></scan:ScanJob>'
elif scan_type == 'jpeg':
    print('Running an image scan...')
    post_body = '<scan:ScanJob xmlns:scan="http://www.hp.com/schemas/imaging/con/cnx/scan/2008/08/19" xmlns:dd="http://www.hp.com/schemas/imaging/con/dictionaries/1.0/" xmlns:fw="http://www.hp.com/schemas/imaging/con/firewall/2011/01/05"><scan:XResolution>600</scan:XResolution><scan:YResolution>600</scan:YResolution><scan:XStart>0</scan:XStart><scan:YStart>0</scan:YStart><scan:Width>1500</scan:Width><scan:Height>2100</scan:Height><scan:Format>Jpeg</scan:Format><scan:CompressionQFactor>0</scan:CompressionQFactor><scan:ColorSpace>Color</scan:ColorSpace><scan:BitDepth>8</scan:BitDepth><scan:InputSource>Platen</scan:InputSource><scan:GrayRendering>NTSC</scan:GrayRendering><scan:ToneMap><scan:Gamma>1000</scan:Gamma><scan:Brightness>1000</scan:Brightness><scan:Contrast>1000</scan:Contrast><scan:Highlite>179</scan:Highlite><scan:Shadow>25</scan:Shadow></scan:ToneMap><scan:ContentType>Photo</scan:ContentType></scan:ScanJob>'
else:
    print(f'Unknown scan type! {scan_type}')
    exit(-1)

jobs_url = "http://192.168.2.19/Scan/Jobs"

post_response = requests.post(jobs_url, data=post_body, verify=False)
print(post_response)
location = post_response.headers["location"]

# A little too fast for the poor printer
time.sleep(1)

job_id = location.split('/')[-1]
url = jobs_url + "/" + job_id + "/Pages/1"
get_response = requests.get(url, verify=False)

random = str(uuid.uuid4())
name = "scanned-" + random + "." + scan_type.lower()
print(name)

if scan_type == 'pdf':
    document_backup(name, get_response)
elif scan_type == 'jpeg':
    image_backup(name, get_response)

print('Finished scanning, cleaning files...')
os.remove(name)
