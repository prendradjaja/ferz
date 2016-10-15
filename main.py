import requests

j = requests.get('https://en.lichess.org/api/user/thibault').json()
print(j)
