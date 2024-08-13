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

HOST_ADDRESS='192.168.2.19'
JOBS_URL = "http://" + HOST_ADDRESS + "/Scan/Jobs"


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


def get_file_name(scan_type):
    random = str(uuid.uuid4())
    name = "scanned-" + random + "." + scan_type
    print(name)
    return name


def format_body_content(output_type, resolution):
    resolution_values = {'high': {'width': 2550, 'length': 3300, 'resolution': 600}, 'low': {'width': 1500, 'length': 3000, 'resolution': 300}}
    format = {'pdf': 'Pdf', 'jpeg': 'Jpeg'}
    content_type = {'pdf': 'Document', 'jpeg': 'Photo'}
    post_body = '<scan:ScanJob xmlns:scan="http://www.hp.com/schemas/imaging/con/cnx/scan/2008/08/19" xmlns:dd="http://www.hp.com/schemas/imaging/con/dictionaries/1.0/" xmlns:fw="http://www.hp.com/schemas/imaging/con/firewall/2011/01/05"> <scan:XResolution>{{ resolution }}</scan:XResolution> <scan:YResolution>{{ resolution }}</scan:YResolution> <scan:XStart>0</scan:XStart> <scan:YStart>0</scan:YStart> <scan:Width>{{ width }}</scan:Width> <scan:Height>{{ height }}</scan:Height> <scan:Format>{{ format }}</scan:Format> <scan:CompressionQFactor>0</scan:CompressionQFactor> <scan:ColorSpace>Color</scan:ColorSpace> <scan:BitDepth>8</scan:BitDepth> <scan:InputSource>Platen</scan:InputSource> <scan:GrayRendering>NTSC</scan:GrayRendering> <scan:ToneMap> <scan:Gamma>1000</scan:Gamma> <scan:Brightness>1000</scan:Brightness> <scan:Contrast>1000</scan:Contrast> <scan:Highlite>179</scan:Highlite> <scan:Shadow>25</scan:Shadow> </scan:ToneMap> <scan:ContentType>{{ content_type }}</scan:ContentType> </scan:ScanJob>'

    post_body.replace('{{ resolution }}', resolution_values[resolution]['resolution'])
    post_body.replace('{{ width }}', resolution_values[resolution]['width'])
    post_body.replace('{{ length }}', resolution_values[resolution]['length'])
    post_body.replace('{{ format }}', format[output_type])
    post_body.replace('{{ content_type }}', content_type[output_type])


def send_job_request(output_type, resolution):
    print("Running scan type " + output_type)
    post_body = format_body_content(output_type, resolution)
    post_response = requests.post(JOBS_URL, data=post_body, verify=False)
    print(post_response)
    location = post_response.headers["location"]
    return location


def get_printer_result(location):
    job_id = location.split('/')[-1]
    url = JOBS_URL + "/" + job_id + "/Pages/1"
    return requests.get(url, verify=False)


def save_file(destination, name, get_response):
    if destination == 'docs':
        document_backup(name, get_response)
    elif destination == 'images':
        image_backup(name, get_response)


parser = argparse.ArgumentParser("scanner_runner")
parser.add_argument("-o", "output_type", help="What kind of scan will it be? pdf, jpeg", type=str)
parser.add_argument("-d", "destination", help="Which folder will it go to? docs images", type=str)
parser.add_argument("resolution", help="High or Low Resolution? high low", type=str)
args = parser.parse_args()

output_type = args.output_type.lower()
resolution = args.resolution.lower()
destination = args.destination.lower()


# Send the request, get the redirect response
location = send_job_request(output_type, resolution)

# A little too fast for the poor printer
time.sleep(1)

get_response = get_printer_result(location)

name = get_file_name(output_type)

save_file(destination, name, get_response)

print('Finished scanning, cleaning files...')
os.remove(name)
