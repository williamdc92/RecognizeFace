import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


KEY = "KEY"

ENDPOINT = "https://ENDPOINT.cognitiveservices.azure.com/"

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

single_face_image_url = 'https://thumbs.dreamstime.com/z/foto-di-due-persone-emozionate-e-divertenti-che-festeggiano-l-estasiata-brunetta-alla-moda-si-sono-divertite-con-qualcosa-158403361.jpg'
single_image_name = os.path.basename(single_face_image_url)

detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_03')
if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))

print('Detected face ID from', single_image_name, ':')
for face in detected_faces: print (face.face_id)
print()

first_image_face_ID = detected_faces[0].face_id



detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model='detection_03')
if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))

def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))

def drawFaceRectangles() :
    response = requests.get(single_face_image_url)
    img = Image.open(BytesIO(response.content))

    print('Drawing rectangle around face... see popup for results.')
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red')

    img.show()

drawFaceRectangles()