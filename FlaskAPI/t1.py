# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 01:16:23 2020

@author: shahb
"""


import requests
from data_input import data_in
import json

URL = 'http://127.0.0.1:5000/predict'

header = {'Content-Type':'application/json'}
data = {'input':data_in}

r = requests.get(URL,headers=header,json=data)

r.json()