# Template for credentials
import requests, json

## Get list of available tunnels from ngrok API
res = requests.get('http://127.0.0.1:4040/api/tunnels')
https_tunnels = [x for x in json.loads(res.text)['tunnels'] if x['proto'] == 'https']

bot_token = "BOTID:HASH"
bot_user_name = "BOTNAME"
URL = https_tunnels[0]['public_url'] # get the first HTTPS tunnel

print('Using URL '+URL)
