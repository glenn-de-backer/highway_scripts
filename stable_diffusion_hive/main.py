#
# Stable diffusion hive
#
# @author Glenn De Backer <glenn.de.backer@student.howest.be>
#  
import requests
import io
import os 
import base64
from PIL import Image, PngImagePlugin

#
# Path to save images (webserver)
TARGET_DIR = "images"

#
# url of the Stable diffusion server
url = "http://127.0.0.1:7860"

#
# @TODO Listen for keyboard/input messages

#
# Payload 
# @TODO process the input of the keyboard here
payload = {
    "prompt": "futuristic highway",
    "steps": 5
}

#
# generate 8 images
for x in range(1,8):
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[1])))

        png_payload = {
            "image": "data:image/png;base64," + i.split(",",1)[1]
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        # save image
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        TARGET_FILE_NAME = os.path.join(TARGET_DIR, "output_%s.png" % x)
        image.save(TARGET_FILE_NAME, pnginfo=pnginfo)