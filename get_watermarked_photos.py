import requests, random
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
from utils import webutils as wu


sites = {
    "shutterstock" : {
        "base_url" : "https://www.shutterstock.com", 
        "url" : "https://www.shutterstock.com/search?searchterm=", 
        "result_class" : "a.js_related-item",
        "image_selector" : "img.img",
        "class": "watermarked"
    },
    "istockphoto" : {
        "base_url" : "https://www.istockphoto.com",
        "url" : "https://www.istockphoto.com/photos/",
        "result_class" : "a.asset-link",
        "image_selector" : ".unzoomed > img:nth-child(1)",
        "class" : "watermarked"
    },
    "freeimages" : {
        "base_url" : "https://www.freeimages.com", 
        "url" : "https://www.freeimages.com/search/", 
        "result_class" : "li.item > a",
        "image_selector" : "a.preview > img",
        "class" : "unwatermarked"
    }
}

words = wu.read_file("wordnouns.txt")
stop_being_a_dumb_bitch = open("output.csv", "w")
usragent={"user-agent": "Mozilla Firefox"}

for word in words:
    for site in sites:
        res = requests.get(sites[site]["url"] + word, headers=usragent)
        soup = BeautifulSoup(res.text, "html.parser")
        sclass = sites[site]["result_class"]
        firstimg=soup.select(sclass)
        try:
            surl = urljoin(sites[site]["base_url"], firstimg[0]['href'])
        except Exception:
            print("GO DO THE CAPTCHA")
            continue
        res = requests.get(surl, headers=usragent)
        soup = BeautifulSoup(res.text, "html.parser")
        simg = sites[site]["image_selector"]
        myimg = soup.select(simg)
        try:
            oput = urljoin(surl, myimg[0]['src']) + ", " + sites[site]["class"]
        except Exception:
            continue
        stop_being_a_dumb_bitch.write(oput)
        stop_being_a_dumb_bitch.write("\n")
        print(oput)
    

stop_being_a_dumb_bitch.close()


