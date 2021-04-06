import sys
import requests

if len(sys.argv) < 2:
    exit("You need more args homie")

uname = sys.argv[1]
with open('api.bearer', 'r') as bearer:
    btoken = bearer.read()
    btoken = f'Bearer {btoken}'
    
headers = {'Authorization' : btoken}
endpoint = f'https://api.twitter.com/1.1/users/show.json?screen_name={uname}'
# print(endpoint, headers)
res = requests.get(endpoint, headers=headers)
udata = res.json()

small_pfp = udata["profile_image_url"]
pfp = small_pfp[:small_pfp.rfind('_')] + small_pfp[small_pfp.rfind('.'):]
print(pfp)
