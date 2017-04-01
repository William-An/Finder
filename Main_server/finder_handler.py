import xml.etree.ElementTree
import requests
import sqlite3
import time
import os
import sys
import numpy as np
# import cv2

# TODO Return search result and store data
"""
Process:
1. get pic_xml
2. identify its key
3. log it in database or later? after step 4
    a. data structure?
4. Post request to google cloud platform
    a. OpenCV process pic: extract major content
    b. Store in google cloud
    c. Call Vision API
    d. Get tag
    e. Pair
5. Get result and store in
6. Return
"""
# Deal with msg

# Do it need to be OO?
# Or can i create a pic_process module?
class handler:
    def __init__(self,xml_root):
        pass
    def request_identifier(self,xml_root):# Necessary?
        pass
    def pic_extractor(self,pic_url): # Merge with cloud_poster?
        pass
    def cloud_poster(self,img_dir):
        pass # delete local image, return gs url
    def img_tagger(self,gs_url):
        pass
    def pair(self):
        pass
        # How???
    def data_log(self):
        pass
