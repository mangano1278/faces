import requests
from lxml import html
import pandas
import re
import json
import datetime
import pprint

def pic_analysis(url):

    if not url[0:7] == "http://":
        url = "http://"+url

    response = requests.get(url)
    doc = html.fromstring(response.text)


    images = doc.findall(".//img")
    data = [a.get("src") for a in images]


    face_image = 0
    num_ppl = 0
    white = 0
    black = 0
    asian = 0
    male = 0
    female = 0
    total_age = 0
    smile_prob = 0

    facepp_url = "https://faceplusplus-faceplusplus.p.mashape.com/detection/detect"

    mashape_key = "IUuNnqMoCQmshbgOtx3gogc2EkAIp1ndau9jsnPnCkuevVPjsz"

    for i in (range(len(data)-7)):
        img_url = data[i]
        headers = {
          "X-Mashape-Key": mashape_key,
          "Accept": "application/json"
        }

        parameters = {
            'attribute': "glass,gender,age,race,smiling",
            'url': img_url
        }

        resp = requests.get(facepp_url, params=parameters, headers=headers)

        output = json.loads(resp.text)

        test = output.keys()
    
        if test[0] == "error_code":
            continue
    
        if not output["face"] == []:
            face_image = face_image + 1
            num_ppl = num_ppl + len(output["face"])

            for x in (range(len(output["face"]))):
                if output["face"][x]["attribute"]["gender"]["value"] == "Male": male = male + 1
                if output["face"][x]["attribute"]["gender"]["value"] == "Female": female = female + 1    
            
                if output["face"][x]["attribute"]["race"]["value"] == "Black" : black = black + 1
                if output["face"][x]["attribute"]["race"]["value"] == "White" : white = white + 1
                if output["face"][x]["attribute"]["race"]["value"] == "Asian" : asian = asian + 1
            
                total_age = total_age + output["face"][x]["attribute"]["age"]["value"]
            
                smile_prob = smile_prob + output["face"][x]["attribute"]["smiling"]["value"]
            
    img_dict = {
    "image_count" :  len(images),
    "people_images" : face_image,
    "ave_ppl_per_img" : 1.0*(num_ppl)/(face_image),
    "total_males" : male,
    "total_females" : female,
    "average_age" : 1.0*(total_age/num_ppl),
    "total_asian" : asian,
    "total_white" : white,
    "total_black" : black,
    "smile_prob" : 1.0*(smile_prob/num_ppl)              
    }
    
    return img_dict

url = raw_input("Please enter a web-page url: ")

pprint.pprint(pic_analysis(url))
