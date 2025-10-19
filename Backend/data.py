import os
import time
import json
import requests
import mimetypes
from dotenv import load_dotenv

load_dotenv()

Astronomy_Api_Key = os.getenv("Astronomy_api")
headers = {"Referer": "https://nova.astrometry.net/api/login"}

def Process_Image(img_uri):

    def Log_in():

        log_in_request = {
            "apikey":Astronomy_Api_Key
        }

        Response = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps(log_in_request)})

        Data = Response.json()
        
        return Data['session']

    Session_Key = Log_in()

    data = {"session": Session_Key}
    uri = "http://nova.astrometry.net/api/upload"   
    
    mimetype, _ = mimetypes.guess_type(img_uri)
    if mimetype is None:
        mimetype = "application/octet-stream"

    with open(img_uri, "rb") as file:
        files = {
            "request-json": (None, json.dumps(data), "text/plain"),
            "file": (img_uri.split("/")[-1], file, mimetype)
        }
        response = requests.post(uri, files=files)

    print(response.status_code)
    print(response.json())
    return response.json()["subid"], Session_Key
    
def Get_Complete_Job(job_id, Session_Key):

    data = {"session": Session_Key}

    Response = requests.post(f'http://nova.astrometry.net/api/jobs/{job_id}/info/', headers=headers)

    print(Response.json())

def Get_Complete_Files(job_id, Session_Key):
    data = {"session": Session_Key}

    base_url = "http://nova.astrometry.net"
    endpoints = [
        f"/annotated_display/{job_id}",
        f"/red_green_image_display/{job_id}",
        f"/extraction_image_display/{job_id}"
    ]

    for endpoint in endpoints:
        url = base_url + endpoint
        response = requests.get(url, headers=headers, stream=True)
        #print(response.text)

        if response.status_code == 200:
            ext = ".png" if "display" in endpoint else ".fits"
            filename = f"./Data/{endpoint.split('/')[-2]}_{job_id}{ext}"
            #filename = "./Data/" + endpoint.split("/")[-2] + f"_{job_id}.fits" if "fits" in endpoint else endpoint.split("/")[-2] + f"_{job_id}.png"
            with open(filename, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print(f"✅ Saved {filename}")
        else:
            print(f"⚠️ Could not download {endpoint} (status: {response.status_code})")

def Check_Status(SUBID):
    URL = f"http://nova.astrometry.net/api/submissions/{SUBID}"
    status = True

    while status:
        response = requests.get(url=URL, headers=headers)
        data = response.json()["job_calibrations"]
        if data == []:
            status = False



Sub_id, Session_Key = Process_Image("./Sample.jpg")
Check_Status(Sub_id)
Get_Complete_Job(Sub_id, Session_Key)
Get_Complete_Files(Sub_id, Session_Key)