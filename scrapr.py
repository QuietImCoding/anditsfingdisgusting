import os, requests, random
import io
import sys

with open('words.txt', 'r') as wfile:
    words = wfile.readlines()
with open('flickr.key', 'r') as fkey:
    flickey = fkey.read()
    
def getOrigImage(img_id):
    minWidth = 300
    minHeight = 300
    flickrhead = {}
    flickrhead['api_key'] = flickey
    flickrhead['method'] = 'flickr.photos.getSizes'
    flickrhead["photo_id"] = str(img_id)
    flickrhead['format'] = 'json'
    flickrhead['nojsoncallback'] = '1'
    fresp = requests.get("https://api.flickr.com/services/rest/", flickrhead)
    try:
        temp = fresp.json()["sizes"]["size"][-1]
        if int(temp['width']) < minWidth or int(temp['height']) < minHeight:
            #print("Image too small")
            return None
        res = temp["source"]
        return res
    except Exception:
        return None

def findImage(windex, debug=False):
    
    word = words[windex % len(words)]

    flickrhead = {}
    flickrhead['api_key'] = flickey
    flickrhead['safe_search'] = '1'
    flickrhead['method'] = 'flickr.photos.search'
    flickrhead['tags'] = word
    flickrhead['format'] = 'json'
    flickrhead['nojsoncallback'] = '1'
    response = requests.get("https://api.flickr.com/services/rest/", flickrhead)
    res = response.json()["photos"]
    if debug:
        print(str(res["page"]))
        print(str(res["pages"]))
        print(str(res["perpage"]))
        print(str(res["total"]))
        for photo in res["photo"]:
            print(str(photo))

    if len(res['photo']) == 0: return None

    photos = []
    for photo in res['photo']:
        photos.append([photo['farm'], photo['server'], photo['id'], photo['secret'], photo['owner']])

    urls = []
    for photo in photos:
        orig = getOrigImage(photo[2])
        if orig is not None: urls.append(orig)

    #print("Got image data for", word)
    return { "word" : word, "urls": urls }

if len(sys.argv) < 2:
    exit('GIB MORE ARGS LOSER')

inval = int(sys.argv[1])
outp = {"urls": []}
while len(outp['urls']) == 0:
    oldp = outp
    outp = findImage(inval)
    if outp is None: outp = oldp
    inval += 1
print(outp['urls'][0])


