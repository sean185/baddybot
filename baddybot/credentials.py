import requests, json
res = requests.get('http://127.0.0.1:4040/api/tunnels')

bot_token = "your-token-here"
bot_user_name = "your-botname-here"
https_tunnels = [x for x in json.loads(res.text)['tunnels'] if x['proto'] == 'https']
URL = https_tunnels[0]['public_url']
print('Using URL '+URL)
