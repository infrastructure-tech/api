import requests

response = requests.post('https://web.infrastructure.tech/wp-json/gf/v2/forms/1/submissions', auth=requests.auth.HTTPBasicAuth('ck_d26f482577ea36ffa415764bf41efb1409a28a6f', 'cs_f62adfee743d2782e0db798deafb1455d0ae5dee'), data={'input_1': 'pytest', 'input_2': "v00.00.02", 'input_5': 'private'}, files={'input_6': open('C:/eons/git/web-infrastructure/plugin_web.infrastructure.tech/generated/web.infrastructure.tech.zip', 'rb')})
print(response)